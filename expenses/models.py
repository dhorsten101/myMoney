from django.db import models


class Expense(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	balance = models.DecimalField(max_digits=20, decimal_places=6)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"{self.name} - {self.balance}"
