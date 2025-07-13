# management/commands/ping_loop.py
import time

from django.core.management.base import BaseCommand

from monitoring.consumers import ping_all


class Command(BaseCommand):
	help = "Ping all IPs in background"
	
	def handle(self, *args, **kwargs):
		ips = ["192.168.1.1", "8.8.8.8", "10.0.0.1"]
		while True:
			ping_all(ips)
			time.sleep(5)
