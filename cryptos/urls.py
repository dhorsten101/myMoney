# urls.py
from django.urls import path

from . import views

urlpatterns = [
	path("asset/", views.asset_list, name="asset_list"),
	path("asset/new/", views.asset_create, name="asset_create"),
	path("asset/<int:id>/edit/", views.asset_update, name="asset_update"),
	path("asset/<int:id>/delete/", views.asset_delete, name="asset_delete"),
]
