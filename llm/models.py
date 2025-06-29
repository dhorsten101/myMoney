# Create your models here.

from django.db import models


class Feedback(models.Model):
	question = models.TextField()
	answer = models.TextField()
	source = models.CharField(max_length=50)
	is_helpful = models.BooleanField()
	created_at = models.DateTimeField(auto_now_add=True)
