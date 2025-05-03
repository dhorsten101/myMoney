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
	return render(request, "dashboard.html")


@login_required
def update_dashboard(request):
	context = process_dashboard_data()  # Get processed data from the utility function
	return render(request, "dashboard.html", context)


@login_required
def assets(request):
	balances = CryptoBalance.objects.all()
	return render(request, "asset_list.html", {"balances": balances})


@login_required
def quote_list(request):
	quotes = Quote.objects.all()
	return render(request, "quote_list.html", {"quotes": quotes})
