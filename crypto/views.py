# views.py
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from crypto.models import CryptoStats


@login_required
def crypto_list(request):
	period = request.GET.get("period", "all")
	now = timezone.now()
	
	if period == "1hour":
		since = now - timedelta(hours=1)
	elif period == "1day":
		since = now - timedelta(days=1)
	elif period == "2day":
		since = now - timedelta(days=2)
	elif period == "1week":
		since = now - timedelta(days=7)
	elif period == "1month":
		since = now - timedelta(days=30)
	elif period == "3month":
		since = now - timedelta(days=90)
	elif period == "6month":
		since = now - timedelta(days=180)
	elif period == "1year":
		since = now - timedelta(days=365)
	else:
		since = None
	
	if since:
		cryptos = CryptoStats.objects.filter(timestamp__gte=since).order_by("-timestamp")
	else:
		cryptos = CryptoStats.objects.order_by("-timestamp")
	
	labels = [crypto.timestamp.strftime("%Y-%m-%d %H:%M") for crypto in cryptos]
	values = [float(crypto.total_value) if crypto.total_value else 0 for crypto in cryptos]
	
	latest_crypto = cryptos.first()
	
	context = {
		"cryptos": cryptos,
		"labels": labels,
		"values": values,
		"crypto": latest_crypto,  # ✅ this is what your template already expects
		"current_period": period,  # optional but needed for highlighting the active filter
	}
	
	return render(request, "crypto_list.html", context)
