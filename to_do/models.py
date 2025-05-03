from django.db import models


class ToDo(models.Model):
	name = models.CharField(max_length=100)
	completed = models.BooleanField(default=False)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"{self.name}"
