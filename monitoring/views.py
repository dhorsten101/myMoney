# views.py
from django.shortcuts import render

from monitoring.admin import MonitoredDevice


def status_view(request):
	devices = MonitoredDevice.objects.all().order_by('ip_address')
	return render(request, 'ping_monitor.html', {'devices': devices})
