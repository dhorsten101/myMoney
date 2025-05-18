# views.py

from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.utils import timezone

from .forms import AssetForm
from .models import Asset, CryptoStats


@login_required
def asset_list(request):
	# Get the period from query params
	period = request.GET.get("period", "1month")
	now = timezone.now()
	
	# Determine start date
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
	
	# --- Asset data ---
	if start_date:
		assets = Asset.objects.filter(timestamp__gte=start_date).order_by("timestamp")
	else:
		assets = Asset.objects.all().order_by("timestamp")
	
	total_balance = assets.aggregate(Sum("balance"))["balance__sum"] or 0
	total_converted_zar = assets.aggregate(Sum("converted_zar"))["converted_zar__sum"] or 0
	total_converted_usd = assets.aggregate(Sum("converted_usd"))["converted_usd__sum"] or 0
	
	asset_labels = [a.timestamp.strftime("%Y-%m-%d") for a in assets]
	asset_values = [float(a.converted_usd) if a.converted_usd else 0 for a in assets]
	
	# --- Crypto data ---
	if start_date:
		cryptos = CryptoStats.objects.filter(timestamp__gte=start_date).order_by("-timestamp")
	else:
		cryptos = CryptoStats.objects.all().order_by("-timestamp")
	
	crypto_labels = [c.timestamp.strftime("%Y-%m-%d %H:%M") for c in cryptos]
	crypto_values = [float(c.total_value) if c.total_value else 0 for c in cryptos]
	latest_crypto = cryptos.first()
	
	# --- Combined context ---
	context = {
		# Assets
		"assets": assets,
		"total_balance": total_balance,
		"total_converted_zar": total_converted_zar,
		"total_converted_usd": total_converted_usd,
		"asset_labels": asset_labels,
		"asset_values": asset_values,
		
		# Cryptos
		"cryptos": cryptos,
		"crypto_labels": crypto_labels,
		"crypto_values": crypto_values,
		"crypto": latest_crypto,
		
		# UI state
		"current_period": period,
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
