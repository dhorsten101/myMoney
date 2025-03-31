# urls.py
from django.urls import path

from . import views

urlpatterns = [
	
	path("idea/", views.idea_list, name="idea_list"),
	path("idea/new/", views.idea_create, name="idea_create"),
	path("idea/<int:id>/edit/", views.idea_update, name="idea_update"),
	path("idea/<int:id>/delete/", views.idea_delete, name="idea_delete"),
]
