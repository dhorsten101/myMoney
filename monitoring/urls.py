# monitoring/urls.py
from django.urls import path

from . import views
from .views import monitoring_view

urlpatterns = [
	path("monitoring/", monitoring_view, name="monitoring"),
	# path("monitor/", views.device_list_view, name="device-list"),
	path("devices/add/", views.add_device_view, name="add-device"),
	path("devices/delete/<int:pk>/", views.delete_device_view, name="delete-device"),
	path("monitoring/api/ping-status/", views.ping_status_api, name="ping-status-api"),
	path("test-socket/", views.test_socket_view, name="test_socket"),
]
