# ping_service.py
from concurrent.futures import ThreadPoolExecutor

from django.utils.timezone import now
from ping3 import ping

from monitoring.admin import MonitoredDevice

MAX_DROP_THRESHOLD = 5


def check_device(device):
	response = ping(device.ip_address, timeout=2)
	if response is None:
		device.drop_count += 1
		if device.drop_count >= MAX_DROP_THRESHOLD:
			device.is_online = False
	else:
		device.drop_count = 0
		device.is_online = True
	device.last_checked = now()
	device.save()


def ping_all_devices():
	devices = MonitoredDevice.objects.all()
	with ThreadPoolExecutor(max_workers=50) as executor:
		executor.map(check_device, devices)
