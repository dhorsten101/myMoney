from django.core.management.base import BaseCommand

from api.utils import process_dashboard_data


class Command(BaseCommand):
	help = "Process dashboard data"
	
	def handle(self, *args, **kwargs):
		self.stdout.write("Starting to process dashboard data...")
		process_dashboard_data()
		self.stdout.write("Dashboard data processed successfully!")
