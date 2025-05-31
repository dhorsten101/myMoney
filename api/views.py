from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from cryptos.crypto import process_crypto_data
from .models import Quote


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
	process_crypto_data()
	return redirect(reverse("asset_list"))


def quote_list(request):
	quotes = Quote.objects.all().order_by('-created_at')
	latest_quote = quotes.first()
	
	return render(request, 'quote_list.html', {
		'quotes': quotes,
		'quote': latest_quote,
	})
