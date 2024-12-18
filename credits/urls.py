# urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("credit/", views.credit_list, name="credit_list"),
    path("credit/new/", views.credit_create, name="credit_create"),
    path("credit/<int:id>/edit/", views.credit_update, name="credit_update"),
    path("credit/<int:id>/delete/", views.credit_delete, name="credit_delete"),
]
