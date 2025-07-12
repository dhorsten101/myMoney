from django.urls import path

from monitoring.views import status_view

urlpatterns = [
	path('status_view', status_view, name='status_view'),

]
