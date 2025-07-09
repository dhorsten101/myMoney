# urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
				  path('document/', views.document_list, name='document_list'),
				  path('document/new/', views.document_create, name='document_create'),
				  path('document/<int:pk>/', views.document_view, name='document_view'),
				  path("document/<int:pk>/edit/", views.document_update, name="document_update"),
				  path("document/<int:pk>/delete/", views.document_delete, name="document_delete"),
			  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
