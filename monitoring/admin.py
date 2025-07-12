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
