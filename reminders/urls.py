from django.urls import path

from . import views

urlpatterns = [
	path('reminders/calendar/', views.calendar_view, name='reminders_calendar'),
	path('reminders/events/', views.events_api, name='reminders_events'),
]


