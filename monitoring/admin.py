from django.contrib import admin

from .models import MonitoredDevice


@admin.register(MonitoredDevice)
class MonitoredDeviceAdmin(admin.ModelAdmin):
	list_display = ("ip_address", "hostname", "is_online", "drop_count", "last_checked")
