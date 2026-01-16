from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView

from logs.views import slow_queries_view
from . import views
from .views import error_log_list, test_error_logging, audit_log_list, logs, service_log_list, global_search, uml_view

urlpatterns = [
	path("", views.home, name="home"),
	path("login/", auth_views.LoginView.as_view(), name="login"),
	path("logout/", auth_views.LogoutView.as_view(), name="logout"),
	path("register/", views.register, name="register"),
	# Simple in-app password reset (no email)
	path("password-reset/", views.password_reset, name="app_password_reset"),
	path("password_reset/", views.password_reset, name="password_reset"),
	path("pricing/", views.pricing, name="pricing"),
	path("contact/", views.contact_view, name="contact"),
	path("error-logs/", error_log_list, name="error_log_list"),
	path("audit-logs/", audit_log_list, name="audit_log_list"),
	path("slow-queries/", slow_queries_view, name="slow_queries"),
	path("service-logs/", service_log_list, name="service_log_list"),
	path('test-log/', test_error_logging, name='test_log'),
	path("logs/", logs, name="logs"),
	path("search/", global_search, name="global_search"),
	path("uml/", uml_view, name="uml_view"),
]
