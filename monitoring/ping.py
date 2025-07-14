# monitoring/services/ping_service.py

import time
from concurrent.futures import ThreadPoolExecutor

import nmap
from django.utils.timezone import now
from ping3 import ping

from monitoring.models import MonitoredDevice, PingResult, PingControl

MAX_DROP_THRESHOLD = 5


def check_device(device):
	try:
		result = ping(device.ip_address, timeout=2)
		success = result is not None
		
		if not success:
			device.drop_count += 1
			if device.drop_count >= MAX_DROP_THRESHOLD:
				device.is_online = False
				device.response_ms = None
		else:
			device.drop_count = 0
			device.is_online = True
			device.response_ms = round(result * 1000, 1)
		
		device.last_checked = now()
		device.save()
		
		PingResult.objects.create(
			device=device,
			success=success,
			latency_ms=(round(result * 1000, 1) if success else None)
		)
	
	except Exception as e:
		print(f"Ping failed for {device.ip_address}: {e}")


# ✅ Add this function right below check_device
def ping_and_log_all_devices():
	devices = MonitoredDevice.objects.all()
	with ThreadPoolExecutor(max_workers=50) as executor:
		executor.map(check_device, devices)


def ping_all_devices():
	devices = MonitoredDevice.objects.all()
	with ThreadPoolExecutor(max_workers=50) as executor:
		executor.map(check_device, devices)


def discover_devices(subnet):
	scanner = nmap.PortScanner()
	scanner.scan(hosts=subnet, arguments="-sn")
	
	added = 0
	for ip in scanner.all_hosts():
		if not MonitoredDevice.objects.filter(ip_address=ip).exists():
			MonitoredDevice.objects.create(ip_address=ip)
			added += 1
	return added


def run_ping_loop():
	print("📡 Ping loop started")
	while PingControl.objects.first().is_running:
		devices = MonitoredDevice.objects.all()
		for device in devices:
			print(f"🔁 Pinging {device.ip_address}")
			latency = ping(device.ip_address, timeout=1)
			is_online = latency is not None
			status = "UP" if is_online else "DOWN"
			
			try:
				PingResult.objects.create(
					device=device,
					latency_ms=round(latency * 1000, 1) if latency else None,
					success=is_online,
					ip=device.ip_address,
					status=status
				)
				print(f"✅ Saved ping for {device.ip_address} - {status}")
			except Exception as e:
				print(f"❌ ERROR saving ping for {device.ip_address}: {e}")
			
			device.is_online = is_online
			device.last_checked = now()
			device.save()
		
		time.sleep(2)
