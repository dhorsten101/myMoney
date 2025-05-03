from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
	path("login/", auth_views.LoginView.as_view(), name="login"),
	path("logout/", auth_views.LogoutView.as_view(), name="logout"),
	path("register/", views.register, name="register"),
	path("pricing/", views.pricing, name="pricing"),
	path("contact/", views.contact_view, name="contact"),
]
