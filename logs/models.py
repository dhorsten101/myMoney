from django.db import models


class SlowQueryLog(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	path = models.CharField(max_length=255)
	duration = models.FloatField()  # request time
	sql_time = models.FloatField()  # total SQL time
	queries = models.TextField()
	
	class Meta:
		ordering = ['-timestamp']
	
	def __str__(self):
		return f"{self.path} - {self.duration}s"
