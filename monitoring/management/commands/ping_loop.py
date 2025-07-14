from django.core.management.base import BaseCommand

from monitoring.ping import run_ping_loop


class Command(BaseCommand):
	help = "Ping all monitored devices continuously unless stopped"
	
	def handle(self, *args, **kwargs):
		print("🟢 Ping loop started")
		run_ping_loop()
