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
	# Return a wide window so you see entries while testing
	now = timezone.now()
	end = now + timedelta(days=365)
	items = Reminder.objects.filter(due_at__gte=now - timedelta(days=365), due_at__lte=end)
	events = []
	for r in items:
		start = r.start_at or r.due_at
		end_time = r.end_at
		evt = {
			'title': r.title,
			'start': start.isoformat(),
			'extendedProps': {
				'description': r.description,
				'severity': r.severity,
				'source': r.source_app,
				'id': r.id,
			}
		}
		if end_time:
			evt['end'] = end_time.isoformat()
		events.append(evt)
	return JsonResponse(events, safe=False)


def reminder_form(request):
	form = ReminderForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('reminders_calendar')
	return render(request, 'reminders/form.html', {'form': form})


def reminder_edit(request, pk: int):
	obj = Reminder.objects.get(pk=pk)
	form = ReminderForm(request.POST or None, instance=obj)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('reminders_calendar')
	return render(request, 'reminders/form.html', {'form': form})


