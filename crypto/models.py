from django.db import models


class Crypto(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True)
	price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
	exchange = models.CharField(max_length=50, null=True, blank=True)
	balance = models.DecimalField(max_digits=20, decimal_places=6)
	account_id = models.CharField(max_length=255, null=True, blank=True)
	converted_zar = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
	converted_usd = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
	
	timestamp = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"{self.exchange} - {self.name} - {self.balance}"


class CryptoStats(models.Model):
	EXCHANGE_CHOICES = [
		("binance", "Binance"),
		("luno", "Luno"),
	]
	
	total_value = models.DecimalField(max_digits=20, decimal_places=2)
	exchange = models.CharField(max_length=50, choices=EXCHANGE_CHOICES)
	timestamp = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"{self.exchange} - {self.total_value}"
