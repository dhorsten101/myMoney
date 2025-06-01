from decimal import Decimal

from api.binance_service import BinanceService
from api.luno_service import LunoService
from cryptos.models import CryptoStats
from history_records.models import HistoryRecord


def process_crypto_data():
	luno_service = LunoService()
	binance_service = BinanceService()
	
	# Fetch and process Luno balances
	balance = luno_service.get_balance()
	(
		converted_balances,
		exchange_rates_zar,
		zar_to_usd_rate,
		luno_total_converted_zar,
		total_converted_usd,
	) = luno_service.convert_balances_to_currencies(balance)
	
	luno_service.save_balances_to_model(converted_balances)
	
	# Fetch and process Binance balances
	binance_balances, binance_total_converted_usd, binance_total_converted_zar = (
		binance_service.convert_balances_to_currencies(zar_to_usd_rate)
	)
	binance_service.save_balances_to_model(binance_balances, zar_to_usd_rate)
	
	# Calculate grand total in ZAR
	grand_total_zar = Decimal(str(luno_total_converted_zar)) + Decimal(
		str(binance_total_converted_zar)
	)
	
	# Save grand total to history
	previous_record = CryptoStats.objects.order_by("-timestamp").first()
	if previous_record:
		value_change = grand_total_zar - previous_record.total_value
		went_up = value_change > 0
	else:
		value_change = Decimal(0)
		went_up = None  # No previous record
	
	HistoryRecord.objects.create(total_value=grand_total_zar, category="crypto")
	
	CryptoStats.objects.create(
		total_value=grand_total_zar,
		luno_total_converted_zar=luno_total_converted_zar,
		binance_total_converted_zar=binance_total_converted_zar
	)
