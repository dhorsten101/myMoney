from django.db import models


class WeatherData(models.Model):
	source = models.CharField(max_length=100, default='stormglass')
	air_temperature = models.FloatField(null=True, blank=True)
	water_temperature = models.FloatField(null=True, blank=True)
	dew_point = models.FloatField(null=True, blank=True)
	humidity = models.FloatField(null=True, blank=True)
	pressure = models.FloatField(null=True, blank=True)
	cloud_cover = models.FloatField(null=True, blank=True)
	precipitation = models.FloatField(null=True, blank=True)
	visibility = models.FloatField(null=True, blank=True)
	uv_index = models.FloatField(null=True, blank=True)
	gust = models.FloatField(null=True, blank=True)
	wind_speed = models.FloatField(null=True, blank=True)
	wind_direction = models.FloatField(null=True, blank=True)
	wave_height = models.FloatField(null=True, blank=True)
	wave_direction = models.FloatField(null=True, blank=True)
	wave_period = models.FloatField(null=True, blank=True)
	swell_height = models.FloatField(null=True, blank=True)
	swell_direction = models.FloatField(null=True, blank=True)
	swell_period = models.FloatField(null=True, blank=True)
	secondary_swell_height = models.FloatField(null=True, blank=True)
	secondary_swell_direction = models.FloatField(null=True, blank=True)
	secondary_swell_period = models.FloatField(null=True, blank=True)
	current_speed = models.FloatField(null=True, blank=True)
	current_direction = models.FloatField(null=True, blank=True)
	sea_level = models.FloatField(null=True, blank=True)
	timestamp = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		verbose_name = 'Weather Data'
		verbose_name_plural = 'Weather Data'
		ordering = ['-timestamp']
	
	def __str__(self):
		return f"Weather at {self.timestamp.strftime('%Y-%m-%d %H:%M')} from {self.source}"
