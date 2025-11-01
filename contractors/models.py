from django.db import models


class Contractor(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField(blank=True)
	phone = models.CharField(max_length=50, blank=True)
	company = models.CharField(max_length=200, blank=True)
	service_category = models.CharField(max_length=120, blank=True)
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return self.name or (self.company or "Contractor")
