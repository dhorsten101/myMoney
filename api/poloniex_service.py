import poloniex
from django.conf import settings
from django.utils import timezone

from assets.models import Asset


class PoloniexService:
	def __init__(self):
		self.client = (poloniex.Poloniex({
			'apiKey': settings.POLONIEX_API_KEY,
			'secret': settings.POLONIEX_SECRET_KEY,
		}))
	
	def get_balances(self):
		try:
			balances = self.client.fetch_balance()
			return [
				{"asset": asset, "free": float(balances["free"][asset])}
				for asset in balances["free"]
				if float(balances["free"][asset]) > 0
			]
		except Exception as e:
			print(f"Error fetching Poloniex balances: {e}")
			return []
	
	def get_exchange_rate(self, pair):
		try:
			ticker = self.client.fetch_ticker(pair)
			return float(ticker["last"])
		except Exception as e:
			print(f"Error fetching Poloniex exchange rate for {pair}: {e}")
			return None
	
	def convert_balances_to_currencies(self, zar_to_usd_rate):
		balances = self.get_balances()
		total_converted_usd = 0
		total_converted_zar = 0
		
		# Fetch exchange rates for specific trading pairs
		exchange_rates = {
			"BTC/USDT": self.get_exchange_rate("BTC/USDT"),
			"ETH/USDT": self.get_exchange_rate("ETH/USDT"),
		}
		
		for balance in balances:
			asset = balance["asset"]
			free_balance = float(balance["free"])
			
			if asset == "BTC" and exchange_rates["BTC/USDT"]:
				balance_in_usd = free_balance * exchange_rates["BTC/USDT"]
				balance_in_zar = balance_in_usd * zar_to_usd_rate
			elif asset == "ETH" and exchange_rates["ETH/USDT"]:
				balance_in_usd = free_balance * exchange_rates["ETH/USDT"]
				balance_in_zar = balance_in_usd * zar_to_usd_rate
			else:
				balance_in_usd = 0
				balance_in_zar = 0
			
			total_converted_usd += balance_in_usd
			total_converted_zar += balance_in_zar
			
			balance["converted_usd"] = balance_in_usd
			balance["converted_zar"] = balance_in_zar
		
		return balances, total_converted_usd, total_converted_zar
	
	def save_balances_to_model(self, balance_data):
		for bal in balance_data:
			asset = bal["asset"]
			balance = float(bal["free"])
			usd_value = bal.get("converted_usd", 0)
			zar_value = bal.get("converted_zar", 0)
			
			Asset.objects.update_or_create(
				exchange="Poloniex",
				name=asset,
				defaults={
					"account_id": None,
					"balance": balance,
					"converted_zar": zar_value,
					"converted_usd": usd_value,
					"timestamp": timezone.now(),
				},
			)
