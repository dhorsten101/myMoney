from django.urls import path

from .views import assistant_view

urlpatterns = [
	path("assistant/", assistant_view, name="assistant"),
]
