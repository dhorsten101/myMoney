from django.urls import path

from .views import slow_queries_view

urlpatterns = [
	path('logs/slow-queries', slow_queries_view, name='slow_queries'),
]
