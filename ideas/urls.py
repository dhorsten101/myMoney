# urls.py
from django.urls import path

from . import views

urlpatterns = [
	
	path("idea/", views.idea_list, name="idea_list"),
	path("idea/new/", views.idea_create, name="idea_create"),
	# path("idea/<int:pk>/", views.idea_detail, name="idea_detail"),
	path("idea/<int:id>/edit/", views.idea_update, name="idea_update"),
	path("idea/<int:id>/delete/", views.idea_delete, name="idea_delete"),
	# path("idea/<int:image_id>/delete-image/", views.delete_image, name="delete_image"),
]

# if settings.DEBUG:
# 	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
