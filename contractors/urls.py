from django.urls import path

from contractors import views

urlpatterns = [
	path("contractors/", views.contractor_list, name="contractor_list"),
	path("contractors/new/", views.contractor_create, name="contractor_create"),
	path("contractors/<int:id>/", views.contractor_detail, name="contractor_detail"),
	path("contractors/<int:id>/edit/", views.contractor_update, name="contractor_update"),
	path("contractors/<int:id>/delete/", views.contractor_delete, name="contractor_delete"),
]
