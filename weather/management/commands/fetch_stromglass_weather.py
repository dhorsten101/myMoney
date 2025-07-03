from django.core.management.base import BaseCommand

from weather.weather_service import StormGlassService


class Command(BaseCommand):
	help = "Fetch and store weather data from StormGlass"
	
	def handle(self, *args, **kwargs):
		try:
			service = StormGlassService()
			service.fetch_and_save()
			self.stdout.write(self.style.SUCCESS("✅ Weather data fetched and saved."))
		except Exception as e:
			self.stderr.write(self.style.ERROR(f"❌ Failed to fetch weather data: {e}"))
