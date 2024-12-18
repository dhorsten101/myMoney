from django.urls import path

from . import views

urlpatterns = [
	path("", views.home, name="home"),  # The homepage URL pattern
	path("luno/", views.luno_view, name="luno_view"),
	path("dashboard/", views.dashboard, name="dashboard"),

]
