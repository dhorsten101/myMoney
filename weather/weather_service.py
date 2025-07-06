from datetime import datetime

import requests
from decouple import config

from .models import WeatherData, TideEvent


class StormGlassService:
	BASE_URL = "https://api.stormglass.io/v2/weather/point"
	EXTREMES_URL = "https://api.stormglass.io/v2/tide/extremes/point"
	
	def __init__(self, lat=-34.0507, lng=24.9215):  # Jeffreys Bay default
		self.api_key = config("STORMGLASS_API_KEY")
		self.lat = lat
		self.lng = lng
		self.params = {
			"params": ",".join([
				'airTemperature', 'waterTemperature', 'dewPointTemperature', 'humidity', 'pressure', 'cloudCover', 'dewPointTemperature', 'seaLevel',
				'precipitation', 'visibility', 'gust', 'windSpeed', 'windDirection', 'waveHeight', 'waveDirection', 'wavePeriod', 'swellHeight', 'swellDirection', 'swellPeriod',
			]),
		}
	
	def fetch_and_save(self):
		if not self.api_key:
			raise ValueError("STORMGLASS_API_KEY not set")
		
		response = requests.get(
			self.BASE_URL,
			headers={"Authorization": self.api_key},
			params={**self.params, "lat": self.lat, "lng": self.lng}
		)
		
		if response.status_code != 200:
			raise Exception(f"StormGlass API error: {response.status_code} - {response.text}")
		
		data = response.json()
		
		for entry in data.get("hours", []):
			timestamp = datetime.fromisoformat(entry["time"].replace("Z", "+00:00"))
			WeatherData.objects.update_or_create(
				timestamp=timestamp,
				source="stormglass",
				defaults={
					'air_temperature': entry.get('airTemperature', {}).get('noaa'),
					'water_temperature': entry.get('waterTemperature', {}).get('noaa'),
					'dew_point': entry.get('dewPointTemperature', {}).get('noaa'),
					'humidity': entry.get('humidity', {}).get('noaa'),
					'pressure': entry.get('pressure', {}).get('noaa'),
					'cloud_cover': entry.get('cloudCover', {}).get('noaa'),
					'precipitation': entry.get('precipitation', {}).get('noaa'),
					'visibility': entry.get('visibility', {}).get('noaa'),
					'gust': entry.get('gust', {}).get('noaa'),
					'wind_speed': entry.get('windSpeed', {}).get('noaa'),
					'wind_direction': entry.get('windDirection', {}).get('noaa'),
					'wave_height': entry.get('waveHeight', {}).get('noaa'),
					'wave_direction': entry.get('waveDirection', {}).get('noaa'),
					'wave_period': entry.get('wavePeriod', {}).get('noaa'),
					'swell_height': entry.get('swellHeight', {}).get('noaa'),
					'swell_direction': entry.get('swellDirection', {}).get('noaa'),
					'swell_period': entry.get('swellPeriod', {}).get('noaa'),
					'sea_level': entry.get('seaLevel', {}).get('sg'),
				}
			)
	
	def fetch_tide_extremes(self):
		response = requests.get(
			self.EXTREMES_URL,
			headers={"Authorization": self.api_key},
			params={"lat": self.lat, "lng": self.lng}
		)
		if response.status_code != 200:
			raise Exception(f"Tide extremes API error: {response.status_code} - {response.text}")
		
		for event in response.json().get("data", []):
			TideEvent.objects.update_or_create(
				time=datetime.fromisoformat(event["time"]),
				type=event["type"],
				defaults={
					"height": event.get("height"),
					"source": "stormglass"
				}
			)
