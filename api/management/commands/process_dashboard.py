from django.core.management.base import BaseCommand

from api.utils import process_crypto_data


class Command(BaseCommand):
	help = "Process crypto data"
	
	def handle(self, *args, **kwargs):
		self.stdout.write("Starting to process crypto data...")
		process_crypto_data()
		self.stdout.write("Crypto data processed successfully!")
