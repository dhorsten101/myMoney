from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import CryptoBalance
from .utils import process_dashboard_data


def home(request):
	return render(request, "home.html")


@login_required
def dashboard(request):
	context = process_dashboard_data()  # Get processed data from the utility function
	return render(request, "dashboard.html", context)


@login_required
def assets(request):
	balances = CryptoBalance.objects.all()
	return render(request, "asset_list.html", {"balances": balances})
