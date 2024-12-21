from decimal import Decimal

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from luno_python.client import Client

from history_records.models import HistoryRecord
from .binance_service import BinanceService
from .luno_service import LunoService
from .models import CryptoBalance
from .models import LunoPrice


# from .poloniex_service import PoloniexService


def home(request):
	return render(request, "home.html")


def luno_view(request):
	client = Client(
		api_key_id=settings.LUNO_API_KEY, api_key_secret=settings.LUNO_API_SECRET
	)
	
	# Fetch ticker data for Bitcoin to ZAR
	ticker = client.get_ticker(pair="XBTZAR")
	
	# Save data to the database
	LunoPrice.objects.create(
		pair=ticker["pair"],
		ask_price=ticker["ask"],
		bid_price=ticker["bid"],
		last_trade=ticker["last_trade"],
	)
	
	# Fetch all saved prices
	prices = LunoPrice.objects.all()
	
	return render(request, "luno.html", {"data": prices})


@login_required
def dashboard(request):
	luno_service = LunoService()
	binance_service = BinanceService()
	# poloniex_service = PoloniexService()  # Add Poloniex service
	
	# Fetching Luno balances and conversion
	balance = luno_service.get_balance()
	(
		converted_balances,
		exchange_rates_zar,
		zar_to_usd_rate,
		total_converted_zar,
		total_converted_usd,
	) = luno_service.convert_balances_to_currencies(balance)
	
	luno_service.save_balances_to_model(converted_balances)
	profit_loss_data = luno_service.calculate_profit_loss()
	orders = luno_service.get_orders(state="COMPLETE")
	
	# Fetching Binance balances and conversions
	binance_balances, binance_total_converted_usd, binance_total_converted_zar = (
		binance_service.convert_balances_to_currencies(zar_to_usd_rate)
	)
	binance_service.save_balances_to_model(binance_balances, zar_to_usd_rate)
	
	# Fetching Poloniex balances and conversions
	# poloniex_balances, poloniex_exchange_rates, poloniex_total_zar, poloniex_total_usd = (
	# 	poloniex_service.convert_balances_to_currencies(
	# 		poloniex_service.get_balance()
	# 	)
	# )
	
	# Calculate the grand total in ZAR
	grand_total_zar = (
			Decimal(str(total_converted_zar))
			+ Decimal(str(binance_total_converted_zar))
		# + Decimal(str(poloniex_total_zar))
	)
	
	# Save the grand total to history
	previous_record = HistoryRecord.objects.filter(category="crypto").order_by("-timestamp").first()
	if previous_record:
		value_change = grand_total_zar - previous_record.total_value
		went_up = value_change > 0
	else:
		value_change = Decimal(0)
		went_up = None  # No previous record
	
	HistoryRecord.objects.create(total_value=grand_total_zar, category="crypto")
	grand_total_history = HistoryRecord.objects.filter(category="crypto").order_by("-timestamp")[:15]
	
	context = {
		# Luno data
		"balance": converted_balances,
		"btc_to_zar": exchange_rates_zar["XBT"],
		"eth_to_zar": exchange_rates_zar["ETH"],
		"sol_to_zar": exchange_rates_zar["SOL"],
		"grt_to_zar": exchange_rates_zar["GRT"],
		"trx_to_zar": exchange_rates_zar["TRX"],
		"xrp_to_zar": exchange_rates_zar["XRP"],
		"zar_to_usd_rate": zar_to_usd_rate,
		"total_converted_zar": total_converted_zar,
		"total_converted_usd": total_converted_usd,
		"profit_loss": profit_loss_data["profit_loss"],
		"money_in": profit_loss_data["money_in"],
		"money_out": profit_loss_data["money_out"],
		"combined_balance": profit_loss_data["combined_balance"],
		"exchange_rates_zar": exchange_rates_zar,
		"orders": orders,
		# Binance data
		"binance_balances": binance_balances,
		"binance_total_converted_usd": binance_total_converted_usd,
		"binance_total_converted_zar": binance_total_converted_zar,
		# Poloniex data
		# "poloniex_balances": poloniex_balances,
		# "poloniex_total_zar": poloniex_total_zar,
		# "poloniex_total_usd": poloniex_total_usd,
		# "poloniex_exchange_rates": poloniex_exchange_rates,
		# Total data
		"grand_total_zar": grand_total_zar,
		"grand_total_history": grand_total_history,
		# up or down data
		"value_change": value_change,
		"went_up": went_up,
	}
	
	return render(request, "dashboard.html", context)


@login_required
def binance_dashboard(request):
	binance_service = BinanceService()
	
	balances, total_converted_usd = binance_service.convert_balances_to_currencies(
		zar_to_usd_rate=True
	)
	
	context = {"balances": balances, "total_converted_usd": total_converted_usd}
	
	return render(request, "dashboard.html", context)


@login_required
def assets(request):
	balances = CryptoBalance.objects.all()
	return render(request, "asset_list.html", {"balances": balances})
