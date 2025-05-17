from binance.client import Client
from django.conf import settings
from django.utils import timezone


class BinanceService:
	def __init__(self):
		self.client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET_KEY)
	
	def get_balances(self):
		account_info = self.client.get_account()
		
		# Filter out cryptos with a balance greater than 0
		balances = [
			balance
			for balance in account_info["balances"]
			if float(balance["free"]) > 0
		]
		return balances
	
	def get_exchange_rates(self, pair):
		"""Fetch exchange rates for specific trading pairs from Binance."""
		try:
			ticker = self.client.get_symbol_ticker(symbol=pair)
			return float(ticker["price"])
		except Exception as e:
			print(f"Error fetching Binance exchange rate for {pair}: {e}")
			return None
	
	def convert_balances_to_currencies(self, zar_to_usd_rate):
		"""Convert Binance balances to both USD and ZAR."""
		balances = self.get_balances()
		total_converted_usd = 0
		total_converted_zar = 0
		
		# Fetching exchange rates for the cryptos you're interested in
		exchange_rates = {
			"BTCUSDT": self.get_exchange_rates("BTCUSDT"),
			"ETHUSDT": self.get_exchange_rates("ETHUSDT"),
			"BNBUSDT": self.get_exchange_rates("BNBUSDT"),  # Add BNB support
			# You can add more pairs if needed
		}
		
		for balance in balances:
			crypto = balance["crypto"]
			free_balance = float(balance["free"])
			
			# Convert to USD and then to ZAR using exchange rates
			if crypto == "BTC" and exchange_rates["BTCUSDT"]:
				balance_in_usd = free_balance * exchange_rates["BTCUSDT"]
				balance_in_zar = balance_in_usd * zar_to_usd_rate
			elif crypto == "ETH" and exchange_rates["ETHUSDT"]:
				balance_in_usd = free_balance * exchange_rates["ETHUSDT"]
				balance_in_zar = balance_in_usd * zar_to_usd_rate
			elif crypto == "BNB" and exchange_rates["BNBUSDT"]:
				balance_in_usd = free_balance * exchange_rates["BNBUSDT"]
				balance_in_zar = balance_in_usd * zar_to_usd_rate
			else:
				balance_in_usd = 0
				balance_in_zar = 0
			
			total_converted_usd += balance_in_usd
			total_converted_zar += balance_in_zar
			
			# Store the converted values in the balance dict
			balance["converted_usd"] = balance_in_usd
			balance["converted_zar"] = balance_in_zar
		
		return balances, total_converted_usd, total_converted_zar
	
	def save_balances_to_model(self, balance_data, zar_to_usd_rate):
		"""Save converted balances to the database."""
		for bal in balance_data:  # Iterate over the list of balances
			crypto = bal["crypto"]
			balance = float(bal["free"])
			
			# Use the converted values (USD and ZAR)
			usd_value = bal.get("converted_usd", 0)
			zar_value = bal.get("converted_zar", 0)
			
			# Save or update the balance in the database
			crypto.objects.update_or_create(
				exchange="Binance",  # Specify the exchange name
				name=crypto,
				defaults={  # Fields that should be updated if the record exists
					"account_id": None,
					"balance": balance,
					"converted_zar": zar_value,
					"converted_usd": usd_value,
					"timestamp": timezone.now(),
				},
			)
