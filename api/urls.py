from django.urls import path

from . import views
from .views import system_metrics_view

urlpatterns = [
	path("", views.home, name="home"),
	
	path("dashboard/", views.dashboard, name="dashboard"),
	path("update_dashboard/", views.update_dashboard, name="update_dashboard"),
	
	path("quote/", views.quote_list, name="quote_list"),
	path('metrics/', system_metrics_view, name='system_metrics'),
]
