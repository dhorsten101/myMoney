from django.urls import path

from .views import dev_assistant_view

urlpatterns = [
	path("dev-assistant/", dev_assistant_view, name="dev_assistant"),
]
