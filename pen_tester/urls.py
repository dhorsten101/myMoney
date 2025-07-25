from django.urls import path

from . import views

urlpatterns = [
	path('pen_tester/', views.pen_test_dashboard, name='pen_test_dashboard'),
	path('report/<int:target_id>/', views.report, name='report'),
]
