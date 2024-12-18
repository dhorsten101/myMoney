# urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("expense/", views.expense_list, name="expense_list"),
    path("expense/new/", views.expense_create, name="expense_create"),
    path("expense/<int:id>/edit/", views.expense_update, name="expense_update"),
    path("expense/<int:id>/delete/", views.expense_delete, name="expense_delete"),
]
