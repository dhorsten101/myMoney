from django.db import models


class Reminder(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True, default='')
	due_at = models.DateTimeField()
	source_app = models.CharField(max_length=100, blank=True, default='')
	source_id = models.CharField(max_length=100, blank=True, default='')
	severity = models.CharField(max_length=20, blank=True, default='info')
	is_active = models.BooleanField(default=True)
	sent_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f"{self.title} @ {self.due_at}"


