from django.urls import path

from . import views

urlpatterns = [
	path('pen_tester/', views.pen_test_dashboard, name='pen_test_dashboard'),
	path('report/<int:target_id>/', views.report, name='report'),
	path('discover/', views.discovery_view, name='discovery'),
	path('discover/<int:job_id>/', views.discovery_result, name='discovery_result'),
]
