# urls.py
from django.urls import path

from . import views

urlpatterns = [
	path("todo/", views.todo_list, name="todo_list"),
	path("todo/new/", views.todo_create, name="todo_create"),
	path("todo/<int:id>/edit/", views.todo_update, name="todo_update"),
	path("todo/<int:id>/delete/", views.todo_delete, name="todo_delete"),
]
