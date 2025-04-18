from django.db import models


class Idea(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(max_length=200)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"{self.name} - {self.description}"
