# urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("history_record/", views.history_record_list, name="history_record_list"),
]
