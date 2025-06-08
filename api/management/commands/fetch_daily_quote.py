import time
import traceback

import requests
from django.core.management.base import BaseCommand

from api.models import Quote
from api.utils import log_error_to_db
from main.models import ExternalServiceLog


class Command(BaseCommand):
	help = 'Fetches the daily quote from ZenQuotes API and saves it to the database'
	
	def handle(self, *args, **kwargs):
		url = "https://zenquotes.io/api/today"
		start = time.time()
		status_code = None
		success = False
		error_message = ""
		response_time = None
		
		try:
			request_start = time.time()
			response = requests.get(url, timeout=10)
			response_time = (time.time() - request_start) * 1000
			response.raise_for_status()
			data = response.json()
			
			if data and isinstance(data, list):
				quote_data = data[0]
				text = quote_data.get("q")
				author = quote_data.get("a")
				
				Quote.objects.create(text=text, author=author)
				self.stdout.write(self.style.SUCCESS("Quote saved successfully"))
				success = True
			else:
				self.stdout.write(self.style.WARNING("No data returned from API"))
				error_message = "Empty or malformed response"
			status_code = response.status_code
		
		except Exception as e:
			tb = traceback.extract_tb(e.__traceback__)[-1]
			log_error_to_db(
				exception=e,
				source="cron.fetch_daily_quote",
				severity="ERROR",
				extra_info={
					"method": "GET",
					"status_code": status_code,
					"path": url,
					"user": "system",
					"ip": "127.0.0.1",
					"func_name": tb.name,
					"pathname": tb.filename,
					"lineno": tb.lineno,
				}
			)
			error_message = str(e)
			self.stderr.write(self.style.ERROR(f"Failed to fetch quote: {e}"))
		
		finally:
			# Log the external request regardless of success/failure
			ExternalServiceLog.objects.create(
				name="ZenQuotes",
				url=url,
				method="GET",
				status_code=status_code,
				response_time_ms=response_time,
				execution_time_ms=(time.time() - start) * 1000,
				response_success=success,
				error_message=error_message if not success else None,
			)
