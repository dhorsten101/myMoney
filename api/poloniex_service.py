from poloniex import Poloniex

from .coingecko_service import get_zar_to_usd_rate, fetch_asset_names


class PoloniexService:
	apikey = "BFIB8QLW-D667IHQA-J305ITJG-Q6H2NE9Z"
	secret = "cf810ecf1aa8ad0b66a36bee6d1072bf9e8b0f2935d0062ccc27b506faf092005691650095e4e3309cf15b5d9f2b80870288c94e6bdd3763df9c8b3645999d18"
	
	def __init__(self, apikey=apikey, secret=secret):
		assert apikey and secret, "API key and Secret key must be provided"
		print(f"Using API Key: {apikey}")  # Debugging purposes only
		self.client = Poloniex(apikey, secret)
		
		self.manual_asset_names = {
			"BHC": "Bitcoin Cash",
		}
		
		self.asset_names = fetch_asset_names()
		self.zar_to_usd_rate = get_zar_to_usd_rate()
	
	def get_balance(self):
		balances = self.client.returnBalances()
		for balance in balances["balance"]:
			print(f"Account ID: {balance['account_id']} for Asset: {balance['asset']}")
		return balances
	
	def get_exchange_rate(self):
		ticker = self.client.returnTicker()
		return float(ticker["last_trade"])
	
	def convert_balances_to_currencies(self, balance):
		exchange_rates_zar = {
			"XBT": self.get_exchange_rate(),
			"ETH": self.get_exchange_rate(),
			"SOL": self.get_exchange_rate(),
		}
		
		zar_to_usd_rate = get_zar_to_usd_rate()
		total_converted_zar = 0
		total_converted_usd = 0
		
		for bal in balance["balance"]:
			asset = bal["asset"]
			asset_name = self.manual_asset_names.get(
				asset, self.asset_names.get(asset, "Unknown")
			)
			
			if asset == "ZAR":
				bal["converted_zar"] = float(bal["balance"])
				bal["converted_usd"] = float(bal["balance"]) / zar_to_usd_rate
				total_converted_zar += bal["converted_zar"]
				total_converted_usd += bal["converted_usd"]
			
			elif asset in exchange_rates_zar:
				bal["converted_zar"] = float(bal["balance"]) * exchange_rates_zar[asset]
				bal["converted_usd"] = bal["converted_zar"] / zar_to_usd_rate
				total_converted_zar += bal["converted_zar"]
				total_converted_usd += bal["converted_usd"]
			
			bal["asset_name"] = asset_name
		
		return (
			balance["balance"],
			exchange_rates_zar,
			zar_to_usd_rate,
			total_converted_zar,
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
