import time

import redis
from django.core.management.base import BaseCommand

from monitoring.consumers import ping_all


class Command(BaseCommand):
	help = "Ping all IPs continuously unless stopped"
	
	def handle(self, *args, **kwargs):
		r = redis.Redis()
		ips = ["192.168.1.1", "8.8.8.8", "10.0.0.1"]
		r.set("ping_running", "1")  # auto-run on script start
		print("🟢 Ping loop started")
		
		while True:
			if r.get("ping_running") != b"1":
				print("⏸️ Ping loop paused")
				time.sleep(1)
				continue
			
			ping_all(ips)
			time.sleep(5)
