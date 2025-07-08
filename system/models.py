from django.db import models


class IntegrityScanLog(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	success = models.BooleanField(default=True)
	issues = models.TextField(blank=True)  # store newline-separated list of issues
	
	class Meta:
		ordering = ['-timestamp']
	
	def __str__(self):
		return f"Scan @ {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {'OK' if self.success else 'Issues'}"


class DeploymentLog(models.Model):
	version = models.CharField(max_length=50)
	commit = models.CharField(max_length=40)
	branch = models.CharField(max_length=40)
	deployed_at = models.DateTimeField(auto_now_add=True)
	deployed_by = models.CharField(max_length=100, blank=True)
