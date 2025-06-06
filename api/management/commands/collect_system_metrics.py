import time

import psutil
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from api.models import SystemMetric


class Command(BaseCommand):
	help = 'Collect system metrics (CPU, memory, disk, uptime, network, db latency)'
	
	def handle(self, *args, **options):
		try:
			cpu = psutil.cpu_percent()
			memory = psutil.virtual_memory().percent
			disk = psutil.disk_usage('/').percent
			uptime = int(time.time() - psutil.boot_time())
			net_io = psutil.net_io_counters()
			bytes_sent = net_io.bytes_sent
			bytes_recv = net_io.bytes_recv
			disk_io = psutil.disk_io_counters()
			disk_read = disk_io.read_bytes
			disk_write = disk_io.write_bytes
			
			# Optional: measure DB latency
			from django.db import connection
			start = time.time()
			with connection.cursor() as cursor:
				cursor.execute("SELECT 1")
			end = time.time()
			db_latency_ms = (end - start) * 1000
			
			SystemMetric.objects.create(
				cpu=cpu,
				memory=memory,
				disk=disk,
				uptime_seconds=uptime,
				bytes_sent=bytes_sent,
				bytes_recv=bytes_recv,
				db_latency_ms=db_latency_ms,
				disk_read=disk_read,
				disk_write=disk_write,
				timestamp=now()
			)
			
			self.stdout.write(self.style.SUCCESS("System metrics logged"))
		
		except Exception as e:
			from api.utils import log_error_to_db
			log_error_to_db(
				message="Failed to collect system metrics",
				level="ERROR",
				exception=e,
				module=__name__,
				severity="ERROR",
			)
