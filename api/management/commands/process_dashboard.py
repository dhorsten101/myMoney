from django.core.management.base import BaseCommand

from api.utils import log_error_to_db
from cryptos.crypto import process_crypto_data


class Command(BaseCommand):
	help = "Process crypto data"
	
	def handle(self, *args, **kwargs):
		self.stdout.write("Starting to process crypto data...")
		try:
			process_crypto_data()
			self.stdout.write(self.style.SUCCESS("Crypto data processed successfully!"))
		except Exception as e:
			self.stderr.write(self.style.ERROR(f"Failed to process crypto data: {e}"))
			log_error_to_db(e, source='cron.crypto_data')
