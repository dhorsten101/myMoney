# consumers.py
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import timezone

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from pythonping import ping


class PingConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		await self.channel_layer.group_add("ping_group", self.channel_name)
		await self.accept()
	
	async def disconnect(self, close_code):
		await self.channel_layer.group_discard("ping_group", self.channel_name)
	
	async def ping_update(self, event):
		await self.send(text_data=json.dumps(event["data"]))


def ping_ip(ip):
	response = ping(ip, count=1, timeout=1)
	return {
		"ip": ip,
		"latency": response.rtt_avg_ms if response.success() else None,
		"status": "UP" if response.success() else "DOWN"
	}


def ping_all():
	from monitoring.models import MonitoredDevice
	devices = MonitoredDevice.objects.all()
	results = []
	with ThreadPoolExecutor(max_workers=50) as executor:
		for result in executor.map(ping_ip, [d.ip_address for d in devices]):
			# update DB record
			MonitoredDevice.objects.filter(ip_address=result["ip"]).update(
				is_online=result["status"] == "UP",
				last_checked=timezone.now()
			)
			broadcast_ping(result)


def broadcast_ping(result):
	channel_layer = get_channel_layer()
	async_to_sync(channel_layer.group_send)(
		"ping_group",
		{"type": "ping_update", "data": result}
	)
