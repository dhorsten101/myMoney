# pen_tester/models.py

from django.db import models


class Target(models.Model):
	domain_or_ip = models.CharField(max_length=255)
	submitted_at = models.DateTimeField(auto_now_add=True)
	ip_address = models.GenericIPAddressField()
	is_online = models.BooleanField(default=False)
	last_discovered = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.domain_or_ip


class ScanResult(models.Model):
	target = models.ForeignKey(Target, on_delete=models.CASCADE, related_name='results')
	tool = models.CharField(max_length=50)
	output = models.TextField()
	scanned_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"{self.tool} on {self.target.domain_or_ip}"


class DiscoveryJob(models.Model):
	subnet = models.CharField(max_length=100)
	started_at = models.DateTimeField(auto_now_add=True)
	finished = models.BooleanField(default=False)
	results = models.JSONField(default=list)  # stores list of IPs
	
	def __str__(self):
		return f"{self.subnet} @ {self.started_at}"
