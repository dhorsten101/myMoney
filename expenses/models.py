from django.conf import settings
from django.db import models


class Expense(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expenses", null=True, blank=True)
	name = models.CharField(max_length=100)
	description = models.TextField()
	balance = models.DecimalField(max_digits=20, decimal_places=6)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"{self.name} - {self.balance}"
