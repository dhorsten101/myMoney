from django.db.models import F, ExpressionWrapper, DurationField
from django.db.models.functions import Abs
from django.shortcuts import render
from django.utils.timezone import now, timedelta

from weather.models import WeatherData


def weather_widget(request):
	recent_data = WeatherData.objects.filter(
		timestamp__gte=now() - timedelta(hours=24)
	).order_by('-timestamp')
	
	context = {
		"weather_data": recent_data,
		"latest": recent_data.first() if recent_data else None,
	}
	return render(request, "weather_widget.html", context)


def weather_list(request):
	now_time = now()
	end_time = now_time + timedelta(hours=96)
	
	recent_data = WeatherData.objects.filter(
		timestamp__gte=now_time,
		timestamp__lte=end_time
	).order_by('timestamp')
	
	# Closest to now
	current_weather = (
		recent_data
		.annotate(
			time_diff=ExpressionWrapper(
				Abs(F('timestamp') - now_time),
				output_field=DurationField()
			)
		)
		.order_by('time_diff')
		.first()
	)
	
	current_weather.wind_speed_knots = round(current_weather.wind_speed * 1.94384, 1) if current_weather.wind_speed else None
	
	if current_weather:
		current_weather.wind_speed_knots = mps_to_knots(current_weather.wind_speed)
		current_weather.wind_direction_compass = degrees_to_compass(current_weather.wind_direction)
	
	labels = [d.timestamp.strftime('%a %d %H:%M') for d in recent_data]
	air_temps = [d.air_temperature for d in recent_data]
	water_temps = [d.water_temperature for d in recent_data]
	humidity = [d.humidity for d in recent_data]
	cloud_cover = [d.cloud_cover for d in recent_data]
	precip = [d.precipitation for d in recent_data]
	
	table_columns = [
		{"slug": "time", "label": "Time", "always_show": True},
		{"slug": "air", "label": "Air Temp °C", "always_show": True},
		{"slug": "water", "label": "Water Temp °C", "always_show": True},
		{"slug": "humidity", "label": "Humidity %", "always_show": True},
		{"slug": "cloud", "label": "Cloud Cover %", "always_show": True},
		{"slug": "precip", "label": "Precip mm", "always_show": True},
		{"slug": "wind", "label": "Wind m/s", "always_show": True},
		{"slug": "winddir", "label": "Wind Dir", "always_show": True},
		{"slug": "wave", "label": "Wave Height m", "always_show": True},
		{"slug": "wavep", "label": "Wave Period s", "always_show": False},
		{"slug": "waved", "label": "Wave Dir", "always_show": False},
		{"slug": "pressure", "label": "Pressure hPa", "always_show": True},
		{"slug": "dew", "label": "Dew Point °C", "always_show": True},
		{"slug": "vis", "label": "Vis km", "always_show": True},
		{"slug": "gust", "label": "Gusts m/s", "always_show": True},
		{"slug": "swellh", "label": "Swell Height m", "always_show": False},
		{"slug": "swellp", "label": "Swell Period s", "always_show": False},
		{"slug": "swelld", "label": "Swell Dir", "always_show": False},
		{"slug": "sea", "label": "Sea Level m", "always_show": True},
	]
	
	context = {
		"weather_data": recent_data,
		"current_weather": current_weather,
		"chart_labels": labels,
		"chart_air_temps": air_temps,
		"chart_water_temps": water_temps,
		"chart_humidity": humidity,
		"chart_cloud": cloud_cover,
		"chart_precip": precip,
		"table_columns": table_columns,
	}
	
	return render(request, "weather_list.html", context)


def mps_to_knots(mps):
	return round(mps * 1.94384, 1) if mps is not None else None


def degrees_to_compass(deg):
	if deg is None:
		return None
	directions = [
		"N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
		"S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
	]
	idx = int((deg + 11.25) / 22.5) % 16
	return directions[idx]
