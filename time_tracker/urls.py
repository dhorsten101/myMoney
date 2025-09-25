from django.urls import path
from . import views

app_name = "time_tracker"

urlpatterns = [
    path("time/", views.dashboard, name="dashboard"),
    path("time/check-in/", views.check_in, name="check_in"),
    path("time/check-out/", views.check_out, name="check_out"),
    path("time/overview/", views.overview, name="overview"),
]
