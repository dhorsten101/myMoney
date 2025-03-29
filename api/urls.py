from django.urls import path

from . import views

urlpatterns = [
	path("", views.home, name="home"),
	path("dashboard/", views.dashboard, name="dashboard"),
	path("update_dashboard/", views.update_dashboard, name="update_dashboard"),

]
