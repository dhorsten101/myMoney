from django.conf import settings
from django.utils import timezone
from luno_python.client import Client

from cryptos.models import Asset
from .coingecko_service import fetch_asset_names, get_zar_to_usd_rate
from .utils import external_service_logger


class LunoService:
	def __init__(self):
		self.client = Client(
			api_key_id=settings.LUNO_API_KEY, api_key_secret=settings.LUNO_API_SECRET
		)
		self.manual_asset_names = {
			"XBT": "Bitcoin",
			"ETH": "Ethereum",
			"SOL": "Solana",
			"GRT": "Graph",
			"TRX": "Tron",
			"XRP": "Ripple",
			"ZAR": "Rands",
		}
		self.asset_names = fetch_asset_names()
		self.zar_to_usd_rate = get_zar_to_usd_rate()
	
	@external_service_logger("Luno - Get Balances", "https://api.luno.com/api/1/balance", method="GET")
	def get_balance(self):
		balances = self.client.get_balances()
		for balance in balances["balance"]:
			print(f"Account ID: {balance['account_id']} for Asset: {balance['asset']}")
		return balances
	
	@external_service_logger("Luno - Get Exchange Rate", "https://api.luno.com/api/1/ticker", method="GET")
	def get_exchange_rate(self, pair):
		ticker = self.client.get_ticker(pair=pair)
		return float(ticker["last_trade"])
	
	def convert_balances_to_currencies(self, balance):
		exchange_rates_zar = {
			"XBT": self.get_exchange_rate("XBTZAR"),
			"ETH": self.get_exchange_rate("ETHZAR"),
			"SOL": self.get_exchange_rate("SOLZAR"),
			"GRT": self.get_exchange_rate("GRTZAR"),
			"TRX": self.get_exchange_rate("TRXZAR"),
			"XRP": self.get_exchange_rate("XRPZAR"),
		}
		
		zar_to_usd_rate = get_zar_to_usd_rate()
		luno_total_converted_zar = 0
		total_converted_usd = 0
		
		for bal in balance["balance"]:
			asset = bal["asset"]
			asset_name = self.manual_asset_names.get(
				asset, self.asset_names.get(asset, "Unknown")
			)
			
			if asset == "ZAR":
				bal["converted_zar"] = float(bal["balance"])
				bal["converted_usd"] = float(bal["balance"]) / zar_to_usd_rate
				luno_total_converted_zar += bal["converted_zar"]
				total_converted_usd += bal["converted_usd"]
			
			elif asset in exchange_rates_zar:
				bal["converted_zar"] = float(bal["balance"]) * exchange_rates_zar[asset]
				bal["converted_usd"] = bal["converted_zar"] / zar_to_usd_rate
				luno_total_converted_zar += bal["converted_zar"]
				total_converted_usd += bal["converted_usd"]
			
			bal["asset_name"] = asset_name
		
		return (
			balance["balance"],
			exchange_rates_zar,
			zar_to_usd_rate,
			luno_total_converted_zar,
			total_converted_usd,
		)
	
	def get_current_combined_balance(self):
		zar_balance = 0
		balances = self.get_balance()
		for balance in balances["balance"]:
			if balance["asset"] == "ZAR":
				zar_balance = float(balance["balance"])
				break
		
		crypto_balance_in_zar = self.calculate_crypto_balances_in_zar()
		return zar_balance + crypto_balance_in_zar
	
	def calculate_crypto_balances_in_zar(self):
		crypto_in_zar = 0
		balances = self.get_balance()
		exchange_rates = {
			"XBT": self.get_exchange_rate("XBTZAR"),
			"ETH": self.get_exchange_rate("ETHZAR"),
			"SOL": self.get_exchange_rate("SOLZAR"),
			"GRT": self.get_exchange_rate("GRTZAR"),
			"TRX": self.get_exchange_rate("TRXZAR"),
			"XRP": self.get_exchange_rate("XRPZAR"),
		}
		
		for balance in balances["balance"]:
			asset = balance["asset"]
			if asset in exchange_rates:
				crypto_in_zar += float(balance["balance"]) * exchange_rates[asset]
		
		return crypto_in_zar
	
	def save_balances_to_model(self, balance_data):
		for bal in balance_data:
			asset = bal["asset"]
			account_id = bal["account_id"]
			balance = float(bal["balance"])
			converted_zar = bal.get("converted_zar", 0)
			converted_usd = bal.get("converted_usd", 0)
			
			Asset.objects.update_or_create(
				exchange="Luno",  # Specify the exchange name
				name=asset,
				defaults={  # Fields that should be updated if the record exists
					"account_id": account_id,  # Binance doesn't have an account_id like Luno
					"balance": balance,
					"converted_zar": converted_zar,
					"converted_usd": converted_usd,
					"timestamp": timezone.now(),
				},
			),
