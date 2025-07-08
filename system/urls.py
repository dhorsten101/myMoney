from django.urls import path

from .views import system, integrity_scan_log_view

urlpatterns = [
	path("system/", system, name="system"),
	path('integrity/logs/', integrity_scan_log_view, name='integrity_scan_logs'),
]
