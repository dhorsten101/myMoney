import psutil
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from api.models import SystemMetric
from api.utils import log_error_to_db


class Command(BaseCommand):
	help = 'Collect CPU, memory, and disk metrics'
	
	def handle(self, *args, **options):
		try:
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
		
		except Exception as e:
			self.stderr.write(self.style.ERROR(f'Failed to log system metrics: {e}'))
			log_error_to_db(e, source='cron.system_metrics')
