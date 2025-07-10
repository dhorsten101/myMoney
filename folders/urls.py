# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import upload_file, folder_list, folder_create, folder_detail, folder_delete, file_delete

urlpatterns = [
				  
				  path('<int:folder_id>/upload/', upload_file, name='upload_file'),
				  
				  path('folder/', folder_list, name='folder_list'),
				  path('folder/new/', folder_create, name='folder_create'),
				  path('folder/<int:pk>/', folder_detail, name='folder_detail'),
				  path('create/', folder_create, name='folder_create'),
				  path('<int:parent_id>/create/', folder_create, name='folder_create_sub'),
				  
				  path('folder/<int:pk>/delete/', folder_delete, name='folder_delete'),
				  path('file/<int:file_id>/delete/', file_delete, name='file_delete'),
			  
			  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
