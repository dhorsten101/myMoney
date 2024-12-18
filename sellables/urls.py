# urls.py
from django.conf.urls.static import static
from django.urls import path

from myMoney import settings
from . import views

urlpatterns = [
	
	path("sellable/", views.sellable_list, name="sellable_list"),
	path("sellable/new/", views.sellable_create, name="sellable_create"),
	path("sellable/<int:pk>/", views.sellable_detail, name="sellable_detail"),
	path("sellable/<int:id>/edit/", views.sellable_update, name="sellable_update"),
	path("sellable/<int:id>/delete/", views.sellable_delete, name="sellable_delete"),
	path("sellable/<int:image_id>/delete-image/", views.delete_image, name="delete_image"),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
