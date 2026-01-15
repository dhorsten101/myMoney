from django.urls import path

from .views import (
	system,
	integrity_scan_log_view,
	user_list,
	user_edit,
	group_list,
	group_create,
	group_edit,
	group_delete,
)

urlpatterns = [
	path("system/", system, name="system"),
	path('integrity/logs/', integrity_scan_log_view, name='integrity_scan_logs'),
	path("system/users/", user_list, name="system_user_list"),
	path("system/users/<int:user_id>/edit/", user_edit, name="system_user_edit"),
	path("system/groups/", group_list, name="system_group_list"),
	path("system/groups/new/", group_create, name="system_group_create"),
	path("system/groups/<int:group_id>/edit/", group_edit, name="system_group_edit"),
	path("system/groups/<int:group_id>/delete/", group_delete, name="system_group_delete"),
]
