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
	recent_data = WeatherData.objects.filter(
		timestamp__gte=now() - timedelta(hours=24)
	).order_by('timestamp')
	
	latest = recent_data.last() if recent_data else None
	
	# Prepare data for Chart.js
	labels = [d.timestamp.strftime('%a %H:%M') for d in recent_data]
	air_temps = [d.air_temperature for d in recent_data]
	wind_speeds = [d.wind_speed for d in recent_data]
	wave_heights = [d.wave_height for d in recent_data]
	
	context = {
		"weather_data": recent_data,
		"latest": latest,
		"chart_labels": labels,
		"chart_air_temps": air_temps,
		"chart_wind_speeds": wind_speeds,
		"chart_wave_heights": wave_heights,
	}
	return render(request, "weather_list.html", context)
