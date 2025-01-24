from django.db import models


class Asset(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	price = models.DecimalField(max_digits=20, decimal_places=8, null=True)
	exchange = models.CharField(max_length=50)
	balance = models.DecimalField(max_digits=10, decimal_places=6)
	account_id = models.CharField(max_length=255, null=True, blank=True)
	converted_zar = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
	converted_usd = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
	
	timestamp = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"{self.exchange} - {self.name} - {self.balance}"
