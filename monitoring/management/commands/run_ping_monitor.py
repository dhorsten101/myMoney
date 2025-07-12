# ping_monitor/management/commands/ping_devices.py
from django.core.management.base import BaseCommand

from monitoring.ping import ping_all_devices


class Command(BaseCommand):
	help = "Ping all monitored devices and update status"
	
	def handle(self, *args, **kwargs):
		ping_all_devices()
		self.stdout.write(self.style.SUCCESS("✅ Ping check completed."))
