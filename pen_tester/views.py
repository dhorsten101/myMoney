# pen_tester/views.py

import json
import socket
import subprocess
import time
from django.utils import timezone

from django.shortcuts import render, redirect, get_object_or_404

from .forms import TargetForm
from .models import DiscoveryJob
from .models import ScanResult, Target


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
		
		docker_cmd = [
			'/usr/bin/docker', 'run', '--rm', '--network=host', 'kali-scanner', subnet
		]
		result = subprocess.run(docker_cmd, capture_output=True, text=True)
		
		try:
			raw_output = result.stdout.strip()
			lines = raw_output.splitlines()
			json_start = next((i for i, line in enumerate(lines) if line.startswith('[')), None)
			
			if json_start is not None:
				cleaned_json = '\n'.join(lines[json_start:])
				ip_list = json.loads(cleaned_json)
				job.results = ip_list
				job.finished = True
				job.save()
				# Create or update targets for each discovered IP
				for ip in ip_list:
					target, _ = Target.objects.get_or_create(
						ip_address=ip,
						defaults={'domain_or_ip': ip, 'is_online': True, 'last_discovered': timezone.now()},
					)
					# If existing, update last_discovered and online flag
					target.is_online = True
					target.last_discovered = timezone.now()
					target.save(update_fields=['is_online', 'last_discovered'])
				return redirect('discovery_result', job_id=job.id)
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


def devices_list(request):
	targets = Target.objects.order_by('-last_discovered', '-last_scanned_at')
	return render(request, 'devices_list.html', {'targets': targets})


def _tcp_port_is_open(ip_address: str, port: int, timeout_seconds: float) -> bool:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(timeout_seconds)
	try:
		start = time.perf_counter()
		sock.connect((ip_address, port))
		# successful connect means port open
		return True
	except Exception:
		return False
	finally:
		try:
			sock.close()
		except Exception:
			pass


def run_basic_scan(request, target_id):
	target = get_object_or_404(Target, id=target_id)
	if request.method != 'POST':
		return redirect('devices_list')
	common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 389, 443, 445, 465, 587, 993, 995, 1433, 1521, 1723, 1883, 2375, 2376, 3000, 3306, 3389, 5000, 5432, 5672, 5900, 5985, 5986, 6379, 7001, 8080, 8081, 8443, 9000, 9200]
	open_ports = []
	latency_ms = 0
	# Measure latency as the fastest successful connect, else 0
	best_latency = None
	for port in common_ports:
		start = time.perf_counter()
		is_open = _tcp_port_is_open(target.ip_address, port, timeout_seconds=0.5)
		elapsed_ms = int((time.perf_counter() - start) * 1000)
		if is_open:
			open_ports.append(port)
			if best_latency is None or elapsed_ms < best_latency:
				best_latency = elapsed_ms
	latency_ms = best_latency or 0
	# Update target summary fields
	target.open_ports = open_ports
	target.port_count = len(open_ports)
	target.is_online = len(open_ports) > 0
	target.latency_ms = latency_ms
	target.last_scanned_at = timezone.now()
	target.save()
	# Store raw scan result
	ScanResult.objects.create(
		target=target,
		tool='basic_tcp_scan',
		output=json.dumps({'open_ports': open_ports, 'latency_ms': latency_ms}),
	)
	return redirect('devices_list')
