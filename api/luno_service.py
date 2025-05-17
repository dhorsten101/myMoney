from django.conf import settings
from django.utils import timezone
from luno_python.client import Client
from luno_python.error import APIError

from .coingecko_service import fetch_crypto_names, get_zar_to_usd_rate


class LunoService:
	def __init__(self):
		self.client = Client(
			api_key_id=settings.LUNO_API_KEY, api_key_secret=settings.LUNO_API_SECRET
		)
		self.manual_crypto_names = {
			"XBT": "Bitcoin",
			"ETH": "Ethereum",
			"SOL": "Solana",
			"GRT": "Graph",
			"TRX": "Tron",
			"XRP": "Ripple",
			"ZAR": "Rands",
		}
		self.crypto_names = fetch_crypto_names()
		self.zar_to_usd_rate = get_zar_to_usd_rate()
	
	def get_balance(self):
		balances = self.client.get_balances()
		for balance in balances["balance"]:
			print(f"Account ID: {balance['account_id']} for crypto: {balance['crypto']}")
		return balances
	
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
		total_converted_zar = 0
		total_converted_usd = 0
		
		for bal in balance["balance"]:
			crypto = bal["crypto"]
			crypto_name = self.manual_crypto_names.get(
				crypto, self.crypto_names.get(crypto, "Unknown")
			)
			
			if crypto == "ZAR":
				bal["converted_zar"] = float(bal["balance"])
				bal["converted_usd"] = float(bal["balance"]) / zar_to_usd_rate
				total_converted_zar += bal["converted_zar"]
				total_converted_usd += bal["converted_usd"]
			
			elif crypto in exchange_rates_zar:
				bal["converted_zar"] = float(bal["balance"]) * exchange_rates_zar[crypto]
				bal["converted_usd"] = bal["converted_zar"] / zar_to_usd_rate
				total_converted_zar += bal["converted_zar"]
				total_converted_usd += bal["converted_usd"]
			
			bal["crypto_name"] = crypto_name
		
		return (
			balance["balance"],
			exchange_rates_zar,
			zar_to_usd_rate,
			total_converted_zar,
			total_converted_usd,
		)
	
	def get_money_in(self):
		total_money_in = 0
		balances = self.get_balance()
		
		try:
			for balance in balances["balance"]:
				account_id = balance["account_id"]  # Use account_id
				print(f"Fetching transactions for account {account_id}")
				
				# Fetch transactions for each account
				transactions = self.client.list_transactions(
					id=account_id, max_row=100, min_row=0
				)
				
				if (
						transactions is None
						or "transactions" not in transactions
						or transactions["transactions"] is None
				):
					print(
						f"No transactions found or transactions is None for account {account_id}"
					)
					continue
				
				for transaction in transactions["transactions"]:
					if transaction["type"] == "DEPOSIT":
						total_money_in += float(transaction["amount"])
					
					# Handle api received transactions (convert to ZAR if needed)
					if transaction["type"] == "RECEIVED":
						amount_zar = float(transaction["amount"]) * float(
							transaction.get("price", 1)
						)
						total_money_in += amount_zar
		
		except APIError as e:
			print(f"Error fetching money in: {e}")
		
		return total_money_in
	
	def get_money_out(self):
		total_money_out = 0
		balances = self.get_balance()
		
		try:
			for balance in balances["balance"]:
				account_id = balance["account_id"]  # Use account_id
				transactions = self.client.list_transactions(
					id=account_id, max_row=100, min_row=0
				)
				
				if (
						transactions is None
						or "transactions" not in transactions
						or transactions["transactions"] is None
				):
					print(
						f"No transactions found or transactions is None for account {account_id}"
					)
					continue
				
				for transaction in transactions["transactions"]:
					if transaction["type"] == "WITHDRAWAL":
						total_money_out -= float(transaction["amount"])
					
					# Handle api sent transactions (convert to ZAR if needed)
					if transaction["type"] == "SENT":
						amount_zar = float(transaction["amount"]) * float(
							transaction.get("price", 1)
						)
						total_money_out -= amount_zar
		
		except APIError as e:
			print(f"Error fetching money out: {e}")
		
		return total_money_out
	
	def calculate_profit_loss(self):
		"""
		Calculate the profit/loss using transactions and orders.
		"""
		money_in = self.get_money_in()
		money_out = self.get_money_out()
		orders = self.get_orders()  # Get completed buy/sell orders
		
		# Ensure 'orders' is a list and not None
		if orders is None:
			orders = []
		
		# Process each order to calculate additional profit/loss
		for order in orders:
			if order["type"] == "BUY":
				# Calculate money spent on buying (added to money_in)
				money_in += float(order["counter"])  # Assuming counter currency is ZAR
			elif order["type"] == "SELL":
				# Calculate money earned from selling (added to money_out)
				money_out += float(order["counter"])  # Assuming counter currency is ZAR
		
		combined_balance = self.get_current_combined_balance()
		profit_loss = combined_balance - (money_in + money_out)
		
		return {
			"profit_loss": profit_loss,
			"money_in": money_in,
			"money_out": money_out,
			"combined_balance": combined_balance,
		}
	
	def get_current_combined_balance(self):
		zar_balance = 0
		balances = self.get_balance()
		for balance in balances["balance"]:
			if balance["crypto"] == "ZAR":
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
			crypto = balance["crypto"]
			if crypto in exchange_rates:
				crypto_in_zar += float(balance["balance"]) * exchange_rates[crypto]
		
		return crypto_in_zar
	
	def get_orders(self, state="COMPLETE"):
		try:
			orders = self.client.list_orders(state=state)
			if orders and "orders" in orders:
				return orders["orders"]  # Return the list of orders
			else:
				print("No orders found.")
				return []
		except APIError as e:
			print(f"Error fetching orders: {e}")
			return []
	
	def save_balances_to_model(self, balance_data):
		for bal in balance_data:
			crypto = bal["crypto"]
			account_id = bal["account_id"]
			balance = float(bal["balance"])
			converted_zar = bal.get("converted_zar", 0)
			converted_usd = bal.get("converted_usd", 0)
			
			crypto.objects.update_or_create(
				exchange="Luno",  # Specify the exchange name
				name=crypto,
				defaults={  # Fields that should be updated if the record exists
					"account_id": account_id,  # Binance doesn't have an account_id like Luno
					"balance": balance,
					"converted_zar": converted_zar,
					"converted_usd": converted_usd,
					"timestamp": timezone.now(),
				},
			),
