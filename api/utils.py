from decimal import Decimal

from poloniex import Poloniex

from history_records.models import HistoryRecord
from .binance_service import BinanceService
from .luno_service import LunoService


def process_dashboard_data():
	polo = Poloniex('F8CU5JIM-6OCAZ7N9-P32460M3-VKCES34I', '444d90c68422d77b1e29c8f72b72c4289d13aa56e76130df2675a8ec0533d0281647fb38819675d9cd665a4e25b6116e89b44bf6182d2aff0e0905d4883e5cdd')
	
	# poloniex_service = PoloniexService()
	luno_service = LunoService()
	binance_service = BinanceService()
	
	# Fetch and process Poloniex balances
	balances = polo.returnBalances()
	print("Balances:", balances)
	
	# Fetch and process Luno balances
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
	
	# Fetch and process Binance balances
	binance_balances, binance_total_converted_usd, binance_total_converted_zar = (
		binance_service.convert_balances_to_currencies(zar_to_usd_rate)
	)
	binance_service.save_balances_to_model(binance_balances, zar_to_usd_rate)
	
	# Calculate grand total in ZAR
	grand_total_zar = Decimal(str(total_converted_zar)) + Decimal(
		str(binance_total_converted_zar)
	)
	
	# Save grand total to history
	previous_record = HistoryRecord.objects.filter(category="crypto").order_by("-timestamp").first()
	if previous_record:
		value_change = grand_total_zar - previous_record.total_value
		went_up = value_change > 0
	else:
		value_change = Decimal(0)
		went_up = None  # No previous record
	
	HistoryRecord.objects.create(total_value=grand_total_zar, category="crypto")
	grand_total_history = HistoryRecord.objects.filter(category="crypto").order_by("-timestamp")[:15]
	
	# Return data for rendering (optional)
	return {
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
		# Total data
		"grand_total_zar": grand_total_zar,
		"grand_total_history": grand_total_history,
		# up or down data
		"value_change": value_change,
		"went_up": went_up,
	}
