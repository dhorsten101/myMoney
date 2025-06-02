import requests
from django.core.management.base import BaseCommand

from api.models import Quote
from api.utils import log_error_to_db


class Command(BaseCommand):
	help = 'Fetches the daily quote from ZenQuotes API and saves it to the database'
	
	def handle(self, *args, **kwargs):
		try:
			response = requests.get("https://zenquotes.io/api/today")
			response.raise_for_status()
			data = response.json()
			
			if data and isinstance(data, list):
				quote_data = data[0]
				text = quote_data.get("q")
				author = quote_data.get("a")
				
				Quote.objects.create(text=text, author=author)
				self.stdout.write(self.style.SUCCESS("Quote saved successfully"))
			else:
				self.stdout.write(self.style.WARNING("No data returned from API"))
		except Exception as e:
			log_error_to_db(e, source="cron.fetch_daily_quote")  # ✅ Save to DB
			self.stderr.write(self.style.ERROR(f"Failed to fetch quote: {e}"))
