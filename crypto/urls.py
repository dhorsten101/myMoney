# urls.py
from django.urls import path

from . import views

urlpatterns = [
	path("crypto/", views.crypto_list, name="crypto_list"),
	# path("crypto/new/", views.crypto_create, name="crypto_create"),
	# path("crypto/<int:id>/edit/", views.crypto_update, name="crypto_update"),
	# path("crypto/<int:id>/delete/", views.crypto_delete, name="crypto_delete"),
]
