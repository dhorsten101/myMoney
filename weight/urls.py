# urls.py
from django.urls import path

from . import views

urlpatterns = [
	path("weight/", views.weight_list, name="weight_list"),
	path("weight/new/", views.weight_create, name="weight_create"),
	path("weight/<int:id>/edit/", views.weight_update, name="weight_update"),
	path("weight/<int:id>/delete/", views.weight_delete, name="weight_delete"),
]
