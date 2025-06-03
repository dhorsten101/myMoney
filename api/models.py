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
	uptime_seconds = models.BigIntegerField(null=True, blank=True)
	bytes_sent = models.BigIntegerField(null=True, blank=True)
	bytes_recv = models.BigIntegerField(null=True, blank=True)
	db_latency_ms = models.FloatField(null=True, blank=True)
	disk_read = models.BigIntegerField(null=True, blank=True, help_text="Disk read bytes")
	disk_write = models.BigIntegerField(null=True, blank=True, help_text="Disk write bytes")
	
	def __str__(self):
		return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - CPU: {self.cpu}%"
