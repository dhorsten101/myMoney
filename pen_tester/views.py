# pen_tester/views.py

import json
import subprocess
import shutil
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import TargetForm
from .models import DiscoveryJob
from .models import Target


def pen_test_dashboard(request):
	form = TargetForm(request.POST or None)
	if form.is_valid():
		target = form.save()
		return redirect('report', target_id=target.id)
	
	targets = Target.objects.order_by('-submitted_at')
	return render(request, 'pen_test_dashboard.html', {
		'form': form,
		'targets': targets,
	})


def report(request, target_id):
	target = get_object_or_404(Target, id=target_id)
	return render(request, 'pen_test_report.html', {
		'target': target,
		'results': target.results.all(),
	})


def discovery_view(request):
	if request.method == 'POST':
		subnet = request.POST.get('subnet')
		job = DiscoveryJob.objects.create(subnet=subnet)
		# Resolve docker binary dynamically
		docker_path = shutil.which('docker')
		if not docker_path:
			job.results = ["Docker not found on PATH"]
			job.finished = True
			job.save()
			return render(request, 'endpoint_discovery.html', {
				'error': 'Docker not found. Please install Docker Desktop or add docker to PATH.',
				'job': job
			})
		
		docker_cmd = [docker_path, 'run', '--rm', '--network=host', 'kali-scanner', subnet]
		result = subprocess.run(docker_cmd, capture_output=True, text=True)
		
		try:
			raw_output = result.stdout.strip()
			lines = raw_output.splitlines()
			json_start = next((i for i, line in enumerate(lines) if line.startswith('[')), None)
			
			if json_start is not None:
				cleaned_json = '\n'.join(lines[json_start:])
				ip_list = json.loads(cleaned_json)
				# Keep only actually reachable hosts by probing common ports briefly
				reachable = _filter_reachable_hosts(ip_list)
				job.results = reachable
				job.finished = True
				job.save()
				# Upsert targets for discovered IPs and mark others offline
				Target.objects.exclude(ip_address__in=reachable).update(is_online=False)
				for ip in reachable:
					target, _ = Target.objects.get_or_create(
						ip_address=ip,
						defaults={'domain_or_ip': ip}
					)
					target.is_online = True
					target.last_discovered = timezone.now()
					target.save(update_fields=['is_online', 'last_discovered', 'domain_or_ip'])
				# Immediately run basic scans for all discovered IPs via Kali and store results
				from .models import ScanResult
				scan_results = run_kali_scan_many(reachable)
				for result in scan_results:
					ip = result.get('ip')
					if not ip:
						continue
					t = Target.objects.filter(ip_address=ip).first()
					if not t:
						continue
					ScanResult.objects.create(target=t, tool='kali_basic_many', output=json.dumps(result))
				return redirect('device_summary')
			else:
				raise ValueError("No valid JSON found in output.")
		
		except Exception as e:
			job.results = [f"Error parsing results: {str(e)}"]
			job.finished = True
			job.save()
			return render(request, 'endpoint_discovery.html', {
				'error': f"Parsing error: {str(e)}",
				'job': job
			})
	
	return render(request, 'endpoint_discovery.html')


def discovery_result(request, job_id):
	job = get_object_or_404(DiscoveryJob, id=job_id)
	return render(request, 'discovery_result.html', {'job': job})


def run_kali_basic_scan(ip: str) -> dict:
	docker_path = shutil.which('docker')
	if not docker_path:
		return {'error': 'Docker not found'}
	cmd = [docker_path, 'run', '--rm', '--network=host', 'kali-scanner', 'python3', 'run_basic_scan.py', ip]
	res = subprocess.run(cmd, capture_output=True, text=True)
	try:
		return json.loads(res.stdout.strip())
	except Exception:
		return {'error': 'Failed to parse scan output', 'raw': res.stdout}


def run_kali_scan_many(ips: list[str]) -> list[dict]:
	docker_path = shutil.which('docker')
	if not docker_path:
		return []
	cmd = [docker_path, 'run', '--rm', '--network=host', 'kali-scanner', 'python3', 'run_scan_many.py'] + ips
	res = subprocess.run(cmd, capture_output=True, text=True)
	try:
		return json.loads(res.stdout.strip())
	except Exception:
		return []


def device_summary(request):
	devices = []
	for target in Target.objects.filter(is_online=True):
		latest = target.results.order_by('-scanned_at').first()
		entry = {
			'id': target.id,
			'ip': target.ip_address,
			'when': latest.scanned_at if latest else None,
			'open_ports_count': 0,
			'example_services': [],
		}
		if latest:
			try:
				data = json.loads(latest.output)
				entry['open_ports_count'] = len(data.get('open_ports', []))
				entry['example_services'] = data.get('open_ports', [])[:3]
			except Exception:
				pass
		devices.append(entry)
	return render(request, 'device_summary.html', {'devices': devices})


def scan_device(request, ip):
	if request.method != 'POST':
		return redirect('device_summary')
	data = run_kali_basic_scan(ip)
	target = Target.objects.filter(ip_address=ip).first()
	if target:
		from .models import ScanResult
		ScanResult.objects.create(target=target, tool='kali_basic', output=json.dumps(data))
	return redirect('device_summary')


def scan_all_devices(request):
	if request.method != 'POST':
		return redirect('device_summary')
	for target in Target.objects.filter(is_online=True):
		data = run_kali_basic_scan(target.ip_address)
		from .models import ScanResult
		ScanResult.objects.create(target=target, tool='kali_basic', output=json.dumps(data))
	return redirect('device_summary')


def _tcp_port_open(ip: str, port: int, timeout_seconds: float = 0.2) -> bool:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(timeout_seconds)
	try:
		return sock.connect_ex((ip, port)) == 0
	except Exception:
		return False
	finally:
		try:
			sock.close()
		except Exception:
			pass


def _ip_is_reachable(ip: str) -> bool:
	# Probe a handful of very common ports quickly
	for port in (22, 80, 443, 445, 139, 53):
		if _tcp_port_open(ip, port):
			return True
	return False


def _filter_reachable_hosts(ip_list):
	if not ip_list:
		return []
	results = []
	max_workers = min(128, max(16, len(ip_list)))
	with ThreadPoolExecutor(max_workers=max_workers) as executor:
		future_map = {executor.submit(_ip_is_reachable, ip): ip for ip in ip_list}
		for future in as_completed(future_map):
			ip = future_map[future]
			try:
				if future.result():
					results.append(ip)
			except Exception:
				pass
	return sorted(results)
