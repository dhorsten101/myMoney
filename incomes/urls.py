# urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("income/", views.income_list, name="income_list"),
    path("income/new/", views.income_create, name="income_create"),
    path("income/<int:id>/edit/", views.income_update, name="income_update"),
    path("income/<int:id>/delete/", views.income_delete, name="income_delete"),
]
