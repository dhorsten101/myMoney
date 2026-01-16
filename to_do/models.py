from django.conf import settings
from django.db import models


class ToDo(models.Model):
	PRIORITY_LOW = "low"
	PRIORITY_HIGH = "high"
	PRIORITY_CHOICES = [
		(PRIORITY_LOW, "Low"),
		(PRIORITY_HIGH, "High"),
	]

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="todos", null=True, blank=True)
	name = models.CharField(max_length=100)
	priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_LOW)
	completed = models.BooleanField(default=False)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"{self.name}"
