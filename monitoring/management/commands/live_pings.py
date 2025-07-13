import time

from django.core.management.base import BaseCommand

from monitoring.models import PingControl
from monitoring.ping import ping_all_devices


class Command(BaseCommand):
	help = "Continuously ping devices if control flag is enabled."
	
	def handle(self, *args, **kwargs):
		self.stdout.write("🔁 Starting ping loop...")
		while True:
			if PingControl.get_state().is_running:
				ping_all_devices()
			time.sleep(1)  # every second
