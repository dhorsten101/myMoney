# models.py
from django.db import models


class MonitoredDevice(models.Model):
	ip_address = models.GenericIPAddressField(unique=True)
	hostname = models.CharField(max_length=255, blank=True, null=True)
	is_online = models.BooleanField(default=True)
	drop_count = models.PositiveIntegerField(default=0)
	last_checked = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"{self.ip_address} ({'Online' if self.is_online else 'Down'})"


# monitoring/models.py

class PingResult(models.Model):
	device = models.ForeignKey(MonitoredDevice, on_delete=models.CASCADE, related_name="ping_results")
	latency_ms = models.FloatField(null=True, blank=True)
	success = models.BooleanField(default=False)
	ip = models.GenericIPAddressField()
	status = models.CharField(max_length=10)
	latency = models.FloatField(null=True)
	active = models.BooleanField(default=False)
	
	timestamp = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['-timestamp']
	
	def __str__(self):
		return f"{self.device.ip_address} @ {self.timestamp} - {'UP' if self.success else 'DOWN'}"


class PingControl(models.Model):
	is_running = models.BooleanField(default=False)
	
	def __str__(self):
		return "Running" if self.is_running else "Stopped"
	
	@classmethod
	def get_state(cls):
		return cls.objects.first() or cls.objects.create(is_running=False)
