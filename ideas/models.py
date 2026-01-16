from django.conf import settings
from django.db import models


class Idea(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ideas", null=True, blank=True)
	name = models.CharField(max_length=100)
	description = models.TextField(max_length=200)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"{self.name} - {self.description}"
