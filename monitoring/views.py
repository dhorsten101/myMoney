# monitoring/views.py
import threading

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from monitoring.models import MonitoredDevice, PingControl
from monitoring.ping import discover_devices, ping_and_log_all_devices, run_ping_loop
from .forms import MonitoredDeviceForm
from .forms import SubnetDiscoveryForm


def start_pings(request):
	# Set control flag
	PingControl.objects.update_or_create(defaults={"active": True})
	
	# Launch background thread
	thread = threading.Thread(target=run_ping_loop)
	thread.daemon = True
	thread.start()
	
	messages.success(request, "▶️ Ping loop started.")
	return redirect("monitoring")


def stop_pings(request):
	PingControl.objects.update_or_create(defaults={"active": False})
	messages.warning(request, "⏹ Ping loop stopped.")
	return redirect("monitoring")


def ping_status_api(request):
	data = []
	for device in MonitoredDevice.objects.all():
		last_ping = device.ping_results.first()  # latest ping
		data.append({
			"ip": device.ip_address,
			"hostname": device.hostname,
			"is_online": device.is_online,
			"latency": last_ping.latency_ms if last_ping else None,
			"loss": device.ping_results.filter(success=False)[:5].count(),
			"last_checked": device.last_checked.strftime("%Y-%m-%d %H:%M:%S"),
		})
	return JsonResponse({"devices": data})


def device_list_view(request):
	devices = MonitoredDevice.objects.all().order_by("ip_address")
	form = MonitoredDeviceForm()
	return render(request, "ping_monitor.html", {"devices": devices, "form": form})


def add_device_view(request):
	if request.method == "POST":
		form = MonitoredDeviceForm(request.POST)
		if form.is_valid():
			form.save()
	return redirect("device-list")


def delete_device_view(request, pk):
	device = get_object_or_404(MonitoredDevice, pk=pk)
	device.delete()
	return redirect("device-list")


def monitoring_view(request):
	subnet_form = SubnetDiscoveryForm()
	
	if request.method == "POST":
		action = request.POST.get("action")
		
		# 🔍 Subnet Discovery
		if not action:
			subnet_form = SubnetDiscoveryForm(request.POST)
			if subnet_form.is_valid():
				subnet = subnet_form.cleaned_data["subnet"]
				added = discover_devices(subnet)
				messages.success(request, f"✅ Discovered and added {added} new device(s) from {subnet}")
				return redirect("monitoring")
		
		# ⚡ Run Pings
		elif action == "run_pings":
			ping_and_log_all_devices()
			messages.success(request, "✅ Pings complete.")
			return redirect("monitoring")
	
	# GET view
	devices = MonitoredDevice.objects.prefetch_related("ping_results").order_by("ip_address")
	return render(request, "ping_monitor.html", {
		"devices": devices,
		"subnet_form": subnet_form
	})


def test_socket_view(request):
	return render(request, "test_socket.html")
