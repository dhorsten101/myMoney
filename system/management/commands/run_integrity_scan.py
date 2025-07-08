from django.core.management.base import BaseCommand
from django.db import models
from django.db.models import Q

from cryptos.models import Asset, CryptoStats
from system.models import IntegrityScanLog
from weather.models import WeatherData, TideEvent


class Command(BaseCommand):
	help = "Runs extended integrity checks on Asset, CryptoStats, WeatherData, and TideEvent models."
	
	def handle(self, *args, **kwargs):
		errors = []
		
		self.stdout.write("🔍 Running extended database integrity scan...\n")
		
		# --- ASSET CHECKS ---
		dup_assets = Asset.objects.values('name').annotate(count=models.Count('id')).filter(count__gt=1)
		if dup_assets.exists():
			dups = ", ".join(d['name'] for d in dup_assets)
			errors.append(f"❌ Duplicate asset names found: {dups}")
		
		no_name = Asset.objects.filter(Q(name__isnull=True) | Q(name=""))
		if no_name.exists():
			errors.append(f"❌ {no_name.count()} assets have no name set")
		
		missing_balances = Asset.objects.filter(balance__isnull=True)
		if missing_balances.exists():
			errors.append(f"❌ {missing_balances.count()} assets have missing balance values")
		
		zero_balance = Asset.objects.filter(balance=0)
		if zero_balance.exists():
			errors.append(f"⚠️ {zero_balance.count()} assets have zero balance")
		
		negative_balance = Asset.objects.filter(balance__lt=0)
		if negative_balance.exists():
			errors.append(f"❌ {negative_balance.count()} assets have negative balances")
		
		inconsistent_currency = Asset.objects.filter(
			Q(converted_zar__isnull=True) | Q(converted_usd__isnull=True)
		)
		if inconsistent_currency.exists():
			errors.append(f"❌ {inconsistent_currency.count()} assets missing currency conversion values")
		
		# --- CRYPTOSTATS CHECKS ---
		negative_total = CryptoStats.objects.filter(total_value__lt=0)
		if negative_total.exists():
			errors.append(f"❌ {negative_total.count()} CryptoStats entries have negative total value")
		
		zero_total = CryptoStats.objects.filter(total_value=0)
		if zero_total.exists():
			errors.append(f"⚠️ {zero_total.count()} CryptoStats entries have total value = 0")
		
		missing_binance = CryptoStats.objects.filter(binance_total_converted_zar__isnull=True)
		if missing_binance.exists():
			errors.append(f"❌ {missing_binance.count()} CryptoStats missing Binance ZAR value")
		
		missing_luno = CryptoStats.objects.filter(luno_total_converted_zar__isnull=True)
		if missing_luno.exists():
			errors.append(f"❌ {missing_luno.count()} CryptoStats missing Luno ZAR value")
		
		# --- WEATHERDATA CHECKS ---
		missing_temps = WeatherData.objects.filter(
			air_temperature__isnull=True, water_temperature__isnull=True
		)
		if missing_temps.exists():
			errors.append(f"❌ {missing_temps.count()} WeatherData entries missing both air and water temperature")
		
		null_sources = WeatherData.objects.filter(source__isnull=True)
		if null_sources.exists():
			errors.append(f"❌ {null_sources.count()} WeatherData entries have no source")
		
		null_pressure = WeatherData.objects.filter(pressure__isnull=True)
		if null_pressure.exists():
			errors.append(f"⚠️ {null_pressure.count()} WeatherData entries have no pressure reading")
		
		# --- TIDEEVENT CHECKS ---
		invalid_tide_types = TideEvent.objects.exclude(type__in=["low", "high"])
		if invalid_tide_types.exists():
			errors.append(f"❌ {invalid_tide_types.count()} TideEvent entries have invalid type values")
		
		null_heights = TideEvent.objects.filter(height__isnull=True)
		if null_heights.exists():
			errors.append(f"⚠️ {null_heights.count()} TideEvent entries have no height recorded")
		
		# --- SUMMARY OUTPUT ---
		if not errors:
			self.stdout.write(self.style.SUCCESS("✅ All integrity checks passed — no issues found.\n"))
		else:
			self.stdout.write(self.style.ERROR("⚠️ Integrity issues found:\n"))
			for err in errors:
				self.stdout.write(f"- {err}")
				
				IntegrityScanLog.objects.create(
					success=(len(errors) == 0),
					issues="\n".join(errors)
				)
