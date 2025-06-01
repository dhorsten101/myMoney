# models.py
from django.db import models
from django.utils.timezone import now


class Quote(models.Model):
	text = models.TextField()
	author = models.CharField(max_length=255, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"{self.text[:50]} - {self.author}"


class SystemMetric(models.Model):
	cpu = models.FloatField(help_text="CPU usage percentage")
	memory = models.FloatField(help_text="Memory usage percentage")
	disk = models.FloatField(help_text="Disk usage percentage")
	timestamp = models.DateTimeField(default=now)
	
	def __str__(self):
		return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - CPU: {self.cpu}%"
