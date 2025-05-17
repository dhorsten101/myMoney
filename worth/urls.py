# urls.py
from django.urls import path

from . import views

urlpatterns = [
	path("worth/", views.worth_list, name="worth_list"),
	path("worth/new/", views.worth_create, name="worth_create"),
	path("worth/<int:id>/edit/", views.worth_update, name="worth_update"),
	path("worth/<int:id>/delete/", views.worth_delete, name="worth_delete"),
]
