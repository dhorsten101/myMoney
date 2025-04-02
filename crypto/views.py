# views.py
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from crypto.form import CryptoForm
from crypto.models import Crypto


@login_required
def crypto_list(request):
	time_period = request.GET.get("period", "1month")  # default to 1 month
	now = timezone.now()
	
	if time_period == "1week":
		start_date = now - timedelta(weeks=1)
	elif time_period == "1year":
		start_date = now - timedelta(days=365)
	else:  # default 1 month
		start_date = now - timedelta(days=30)
	
	from crypto.models import Crypto
	cryptos = Crypto.objects.filter(timestamp__gte=start_date).order_by("timestamp")
	
	# Totals
	total_balance = cryptos.aggregate(Sum("balance"))["balance__sum"] or 0
	total_converted_zar = cryptos.aggregate(Sum("converted_zar"))["converted_zar__sum"] or 0
	total_converted_usd = cryptos.aggregate(Sum("converted_usd"))["converted_usd__sum"] or 0
	
	# Graph Data
	labels = [crypto.timestamp.strftime("%Y-%m-%d") for crypto in cryptos]
	values = [float(crypto.converted_usd) if crypto.converted_usd else 0 for crypto in cryptos]
	
	context = {
		"cryptos": cryptos,
		"total_balance": total_balance,
		"total_converted_zar": total_converted_zar,
		"total_converted_usd": total_converted_usd,
		"labels": labels,
		"values": values,
		"current_period": time_period,
	}
	
	return render(request, "crypto_list.html", context)


# @login_required
# def asset_list(request):
#     assets = Asset.objects.all()
#
#     # Calculate totals for balance, converted_zar, and converted_usd
#     total_balance = assets.aggregate(Sum("balance"))["balance__sum"] or 0
#     total_converted_zar = (
#         assets.aggregate(Sum("converted_zar"))["converted_zar__sum"] or 0
#     )
#     total_converted_usd = (
#         assets.aggregate(Sum("converted_usd"))["converted_usd__sum"] or 0
#     )
#
#     context = {
#         "assets": assets,
#         "total_balance": total_balance,
#         "total_converted_zar": total_converted_zar,
#         "total_converted_usd": total_converted_usd,
#     }
#
#     return render(request, "asset_list.html", context)


@login_required
def crypto_create(request):
	if request.method == "POST":
		form = CryptoForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("crypto_list")
	else:
		form = CryptoForm()
	return render(request, "crypto_form.html", {"form": form})


@login_required
def crypto_update(request, id):
	crypto = get_object_or_404(Crypto, id=id)
	if request.method == "POST":
		form = CryptoForm(request.POST, instance=crypto)
		if form.is_valid():
			form.save()
			return redirect("crypto_list")
	else:
		form = CryptoForm(instance=crypto)
	return render(request, "crypto_form.html", {"form": form})


@login_required
def crypto_delete(request, id):
	crypto = get_object_or_404(Crypto, id=id)
	if request.method == "POST":
		crypto.delete()
		return redirect("crypto_list")
	return render(request, "crypto_confirm_delete.html", {"crypto": crypto})


from django.shortcuts import render

# Create your views here.
