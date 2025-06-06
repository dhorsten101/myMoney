import requests

from api.utils import external_service_logger


@external_service_logger("CoinGecko - Fetch Coins", "https://api.coingecko.com/api/v3/coins/list")
def fetch_asset_names():
	response = requests.get("https://api.coingecko.com/api/v3/coins/list")
	if response.status_code == 200:
		# Normalize symbols to uppercase for matching
		return {coin['symbol'].upper(): coin['name'] for coin in response.json()}
	else:
		return {}


@external_service_logger("CoinGecko - ZAR to USD", "https://api.coingecko.com/api/v3/exchange_rates")
def get_zar_to_usd_rate():
	# Fetch the ZAR to USD exchange rate from CoinGecko
	response = requests.get("https://api.coingecko.com/api/v3/exchange_rates")
	if response.status_code == 200:
		rates = response.json()
		zar_to_usd = rates['rates']['zar']['value'] / rates['rates']['usd']['value']  # ZAR to USD
		return zar_to_usd
	else:
		return 1
