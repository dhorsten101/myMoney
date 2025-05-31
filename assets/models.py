from django.db import models


class Asset(models.Model):
	name = models.CharField(max_length=100)
	exchange = models.CharField(max_length=50, null=True, blank=True)
	balance = models.DecimalField(max_digits=20, decimal_places=6)
	account_id = models.CharField(max_length=255, null=True, blank=True)
	converted_zar = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
	converted_usd = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
	
	timestamp = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	FULL_NAMES = {
		"XBT": "Bitcoin",
		"ETH": "Ethereum",
		"SOL": "Solana",
		"GRT": "Graph",
		"TRX": "Tron",
		"XRP": "Ripple",
		"ZAR": "Rands",
	}
	
	@property
	def full_name(self):
		return self.FULL_NAMES.get(self.name, self.name)
	
	def __str__(self):
		return f"{self.exchange} - {self.name} - {self.balance}"


class CryptoStats(models.Model):
	total_value = models.DecimalField(max_digits=20, decimal_places=2)
	binance_total_converted_zar = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
	luno_total_converted_zar = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)  # luno
	
	timestamp = models.DateTimeField(auto_now_add=True)
