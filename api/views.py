import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from cryptos.crypto import process_crypto_data
from cryptos.models import CryptoStats  # Import your model
from worth.models import Worth
from .models import Quote
from .models import SystemMetric


def home(request):
	latest_quote = Quote.objects.order_by('-created_at').first()
	latest_crypto = CryptoStats.objects.order_by('-timestamp').first()  # Get most recent
	worth = Worth.objects.order_by('-created_at').first()
	
	return render(request, 'home.html', {
		'quote': latest_quote,
		'crypto': latest_crypto,
		'worth': worth,
	})


@login_required
def dashboard(request):
	return render(request, "dashboards/dashboard.html")


@login_required
def update_dashboard(request):
	process_crypto_data()
	return redirect(reverse("asset_list"))


def quote_list(request):
	quotes = Quote.objects.all().order_by('-created_at')
	latest_quote = quotes.first()
	
	return render(request, 'quote_list.html', {
		'quotes': quotes,
		'quote': latest_quote,
	})


def system_metrics_view(request):
	period = request.GET.get("period", "1month")
	now = timezone.now()
	
	if period == "1hour":
		start_date = now - timedelta(hours=1)
	elif period == "2hour":
		start_date = now - timedelta(hours=2)
	elif period == "6hour":
		start_date = now - timedelta(hours=6)
	elif period == "12hour":
		start_date = now - timedelta(hours=12)
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
	else:
		start_date = None
	
	metrics = SystemMetric.objects.filter(timestamp__gte=start_date).order_by("-timestamp") if start_date else SystemMetric.objects.order_by("-timestamp")
	
	labels = [m.timestamp.strftime('%Y-%m-%d %H:%M') for m in metrics]
	cpu = [m.cpu for m in metrics]
	memory = [m.memory for m in metrics]
	disk = [m.disk for m in metrics]
	
	context = {
		'metrics': metrics,
		'crypto_labels': json.dumps(labels),
		'cpu': json.dumps(cpu),
		'memory': json.dumps(memory),
		'disk': json.dumps(disk),
		"disk_read": [round(m.disk_read / (1024 ** 3), 2) if m.disk_read else 0 for m in metrics],
		"disk_write": [round(m.disk_write / (1024 ** 3), 2) if m.disk_write else 0 for m in metrics],
		"bytes_sent": [round(m.bytes_sent / (1024 ** 3), 2) if m.bytes_sent else 0 for m in metrics],
		"bytes_recv": [round(m.bytes_recv / (1024 ** 3), 2) if m.bytes_recv else 0 for m in metrics],
		'current_period': period
	}
	return render(request, 'metrics/system_metrics.html', context)
