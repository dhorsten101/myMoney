# urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import folder_list, folder_create, folder_detail, upload_file

urlpatterns = [
				  path('', folder_list, name='folder_list'),
				  path('create/', folder_create, name='folder_create'),
				  path('<int:pk>/', folder_detail, name='folder_detail'),
				  path('<int:folder_id>/upload/', upload_file, name='upload_file'),
			  
			  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
