# views.py

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.utils import timezone

from .forms import AssetForm
from .models import Asset, CryptoStats


@login_required
def asset_list(request):
	period = request.GET.get("period", "1month")
	now = timezone.now()
	
	# Time filter
	if period == "1hour":
		start_date = now - timedelta(hours=1)
	elif period == "1day":
		start_date = now - timedelta(days=1)
	elif period == "2day":
		start_date = now - timedelta(days=2)
	elif period == "1week":
		start_date = now - timedelta(weeks=1)
	elif period == "1month":
		start_date = now - timedelta(days=30)
	elif period == "3month":
		start_date = now - timedelta(days=90)
	elif period == "6month":
		start_date = now - timedelta(days=180)
	elif period == "1year":
		start_date = now - timedelta(days=365)
	else:
		start_date = None
	
	# Asset data
	if start_date:
		luno_assets = Asset.objects.filter(exchange="Luno", timestamp__gte=start_date).order_by("timestamp")
		binance_assets = Asset.objects.filter(exchange="Binance", timestamp__gte=start_date).order_by("timestamp")
	else:
		luno_assets = Asset.objects.filter(exchange="Luno").order_by("timestamp")
		binance_assets = Asset.objects.filter(exchange="Binance").order_by("timestamp")
	
	total_balance = luno_assets.aggregate(Sum("balance"))["balance__sum"] or 0
	total_converted_zar = luno_assets.aggregate(Sum("converted_zar"))["converted_zar__sum"] or 0
	total_converted_usd = luno_assets.aggregate(Sum("converted_usd"))["converted_usd__sum"] or 0
	
	# Chart values
	luno_labels = [a.timestamp.strftime("%Y-%m-%d") for a in luno_assets]
	luno_values = [float(a.converted_usd) if a.converted_usd else 0 for a in luno_assets]
	
	binance_labels = [a.timestamp.strftime("%Y-%m-%d") for a in binance_assets]
	binance_values = [float(a.converted_usd) if a.converted_usd else 0 for a in binance_assets]
	
	all_assets = (luno_assets | binance_assets).order_by("timestamp")
	combined_labels = [a.timestamp.strftime("%Y-%m-%d") for a in all_assets]
	combined_values = [float(a.converted_usd) if a.converted_usd else 0 for a in all_assets]
	
	# Crypto data
	if start_date:
		cryptos = CryptoStats.objects.filter(timestamp__gte=start_date).order_by("-timestamp")
	else:
		cryptos = CryptoStats.objects.all().order_by("-timestamp")
	
	crypto_labels = [c.timestamp.strftime("%Y-%m-%d %H:%M") for c in cryptos]
	crypto_values = [float(c.total_value or 0) for c in cryptos]  # combined
	binance_values = [float(c.binance_total_converted_zar or 0) for c in cryptos]
	luno_values = [float(c.luno_total_converted_zar or 0) for c in cryptos]
	
	latest_crypto = cryptos.first()
	
	previous_crypto = cryptos[1] if cryptos.count() > 1 else None
	if previous_crypto:
		value_change = latest_crypto.total_value - previous_crypto.total_value
		went_up = value_change > 0
	else:
		value_change = Decimal(0)
		went_up = None
	
	all_assets = (luno_assets | binance_assets).order_by("-timestamp")
	
	context = {
		"all_assets": all_assets,
		"luno_assets": luno_assets,
		"binance_assets": binance_assets,
		"total_balance": total_balance,
		"total_converted_zar": total_converted_zar,
		"total_converted_usd": total_converted_usd,
		
		"luno_labels": luno_labels,
		"luno_values": luno_values,
		"binance_labels": binance_labels,
		"binance_values": binance_values,
		"combined_labels": combined_labels,
		"combined_values": combined_values,
		
		"cryptos": cryptos,
		"crypto_labels": crypto_labels,
		"crypto_values": crypto_values,
		"crypto": latest_crypto,
		"current_period": period,
		
		"value_change": value_change,
		"went_up": went_up,
	}
	
	return render(request, "asset_list.html", context)


@login_required
def asset_create(request):
	if request.method == "POST":
		form = AssetForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("asset_list")
	else:
		form = AssetForm()
	return render(request, "asset_form.html", {"form": form})


@login_required
def asset_update(request, id):
	asset = get_object_or_404(Asset, id=id)
	if request.method == "POST":
		form = AssetForm(request.POST, instance=asset)
		if form.is_valid():
			form.save()
			return redirect("asset_list")
	else:
		form = AssetForm(instance=asset)
	return render(request, "asset_form.html", {"form": form})


@login_required
def asset_delete(request, id):
	asset = get_object_or_404(Asset, id=id)
	if request.method == "POST":
		asset.delete()
		return redirect("asset_list")
	return render(request, "asset_confirm_delete.html", {"asset": asset})
