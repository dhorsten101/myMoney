from django.urls import path

from . import views

urlpatterns = [
	path("", views.camera_list, name="camera_list"),
	path("view/<slug:slug>/", views.camera_view, name="camera_view"),
	path("cameras/new/", views.camera_create, name="camera_create"),
	# path("credit/<int:id>/edit/", views.camera_update, name="camera_update"),
]
