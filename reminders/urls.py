from django.urls import path

from . import views

urlpatterns = [
	path('reminders/calendar/', views.calendar_view, name='reminders_calendar'),
	path('reminders/events/', views.events_api, name='reminders_events'),
	path('reminders/new/', views.reminder_form, name='reminders_new'),
	path('reminders/edit/<int:pk>/', views.reminder_edit, name='reminders_edit'),
]


