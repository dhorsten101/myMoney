from django.db import models


class LunoPrice(models.Model):
	pair = models.CharField(max_length=10)
	ask_price = models.DecimalField(max_digits=10, decimal_places=2)
	bid_price = models.DecimalField(max_digits=10, decimal_places=2)
	last_trade = models.DecimalField(max_digits=10, decimal_places=2)
	timestamp = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"{self.pair} - {self.last_trade}"


class CryptoBalance(models.Model):
	exchange = models.CharField(max_length=50)
	account_id = models.CharField(max_length=255, null=True, blank=True)
	asset = models.CharField(max_length=50)
	balance = models.DecimalField(max_digits=20, decimal_places=8)
	converted_zar = models.DecimalField(max_digits=20, decimal_places=2)
	converted_usd = models.DecimalField(max_digits=20, decimal_places=2)
	timestamp = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"{self.exchange} - {self.asset} - {self.balance}"


class Stats(models.Model):
	exchange = models.CharField(max_length=50)
	zar_to_usd_rate = models.DecimalField(max_digits=20, decimal_places=2)
	total_converted_zar = models.DecimalField(max_digits=20, decimal_places=2)
	total_converted_usd = models.DecimalField(max_digits=20, decimal_places=2)
	balance = models.DecimalField(max_digits=20, decimal_places=8)
	exchange_rates_zar = models.DecimalField(max_digits=20, decimal_places=2)
	orders = models.DecimalField(max_digits=20, decimal_places=2)
	binance_balances = models.DecimalField(max_digits=20, decimal_places=2)
	binance_total_converted_usd = models.DecimalField(max_digits=20, decimal_places=2)
	binance_total_converted_zar = models.DecimalField(max_digits=20, decimal_places=2)
	grand_total_zar = models.DecimalField(max_digits=20, decimal_places=2)
	grand_total_history = models.DecimalField(max_digits=20, decimal_places=2)
	value_change = models.DecimalField(max_digits=20, decimal_places=2)
	went_up = models.DecimalField(max_digits=20, decimal_places=2)
	
	profit_loss = models.CharField(max_length=50)
	money_in = models.CharField(max_length=50)
	money_out = models.CharField(max_length=50)
	combined_balance = models.CharField(max_length=50)
	
	timestamp = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"{self.exchange}"
