from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import error_log_list, test_error_logging, audit_log_list, logs, service_log_list, global_search

urlpatterns = [
	path("login/", auth_views.LoginView.as_view(), name="login"),
	path("logout/", auth_views.LogoutView.as_view(), name="logout"),
	path("register/", views.register, name="register"),
	path("pricing/", views.pricing, name="pricing"),
	path("contact/", views.contact_view, name="contact"),
	path("error-logs/", error_log_list, name="error_log_list"),
	path("audit-logs/", audit_log_list, name="audit_log_list"),
	path("service-logs/", service_log_list, name="service_log_list"),
	path('test-log/', test_error_logging, name='test_log'),
	path("logs/", logs, name="logs"),
	path("search/", global_search, name="global_search"),

]
