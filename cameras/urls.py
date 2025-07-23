from django.urls import path

from . import views

urlpatterns = [
	path("", views.camera_list, name="camera_list"),
	path("view/<slug:slug>/", views.camera_view, name="camera_view"),
]
