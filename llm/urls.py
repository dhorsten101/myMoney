from django.urls import path

from llm.views import assistant_view

urlpatterns = [
	path("assistant/", assistant_view, name="assistant"),
]
