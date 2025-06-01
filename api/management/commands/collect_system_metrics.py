import psutil
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from api.models import SystemMetric


class Command(BaseCommand):
	help = 'Collect CPU, memory, and disk metrics'
	
	def handle(self, *args, **options):
		cpu = psutil.cpu_percent()
		memory = psutil.virtual_memory().percent
		disk = psutil.disk_usage('/').percent
		
		SystemMetric.objects.create(
			cpu=cpu,
			memory=memory,
			disk=disk,
			timestamp=now()
		)
		self.stdout.write(self.style.SUCCESS('System metrics logged'))
