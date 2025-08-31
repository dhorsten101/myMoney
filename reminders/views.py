import json
from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Reminder
from .forms import ReminderForm


def calendar_view(request):
	form = ReminderForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('reminders_calendar')
	return render(request, 'reminders/calendar.html', {'form': form})


def events_api(request):
	# Return the next 60 days of reminders as FullCalendar events
	now = timezone.now()
	end = now + timedelta(days=60)
	items = Reminder.objects.filter(is_active=True, due_at__gte=now - timedelta(days=30), due_at__lte=end)
	events = []
	for r in items:
		events.append({
			'title': r.title,
			'start': r.due_at.isoformat(),
			'extendedProps': {
				'description': r.description,
				'severity': r.severity,
				'source': r.source_app,
				'id': r.id,
			}
		})
	return JsonResponse(events, safe=False)


