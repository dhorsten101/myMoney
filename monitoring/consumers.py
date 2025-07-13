# consumers.py
import json
from concurrent.futures import ThreadPoolExecutor

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


def ping_all(ips):
	results = []
	with ThreadPoolExecutor(max_workers=50) as executor:
		for result in executor.map(ping_ip, ips):
			results.append(result)
			broadcast_ping(result)
	return results


def broadcast_ping(result):
	channel_layer = get_channel_layer()
	async_to_sync(channel_layer.group_send)(
		"ping_group",
		{"type": "ping_update", "data": result}
	)
