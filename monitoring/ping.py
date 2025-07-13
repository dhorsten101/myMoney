# monitoring/services/ping_service.py

from concurrent.futures import ThreadPoolExecutor

import nmap
from django.utils.timezone import now
from ping3 import ping

from monitoring.models import MonitoredDevice, PingResult

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
