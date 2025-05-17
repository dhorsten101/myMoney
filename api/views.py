from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import CryptoBalance, Quote
from .utils import process_dashboard_data


def home(request):
	latest_quote = Quote.objects.order_by('-created_at').first()
	
	return render(request, 'home.html', {
		'quote': latest_quote,
	})


@login_required
def dashboard(request):
	return render(request, "dashboards/dashboard.html")


@login_required
def update_dashboard(request):
	context = process_dashboard_data()  # Get processed data from the utility function
	return render(request, "dashboards/dashboard.html", context)


@login_required
def crypto(request):
	balances = CryptoBalance.objects.all()
	return render(request, "crypto_list.html", {"balances": balances})


def quote_list(request):
	quotes = Quote.objects.all().order_by('-created_at')
	latest_quote = quotes.first()
	
	return render(request, 'quote_list.html', {
		'quotes': quotes,
		'quote': latest_quote,
	})
