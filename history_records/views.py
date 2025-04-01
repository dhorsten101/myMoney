from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone

from .models import HistoryRecord  # adjust if needed


def history_record_list(request):
	period = request.GET.get("period", "all")
	now = timezone.now()
	
	if period == "1hour":
		since = now - timedelta(hours=1)
	elif period == "1day":
		since = now - timedelta(days=1)
	elif period == "2day":
		since = now - timedelta(days=2)
	elif period == "1week":
		since = now - timedelta(days=7)
	elif period == "1month":
		since = now - timedelta(days=30)
	elif period == "3month":
		since = now - timedelta(days=90)
	elif period == "6month":
		since = now - timedelta(days=180)
	elif period == "1year":
		since = now - timedelta(days=365)
	else:
		since = None  # Show all
	
	if since:
		history_records = HistoryRecord.objects.filter(timestamp__gte=since).order_by("-timestamp")
	else:
		history_records = HistoryRecord.objects.order_by("-timestamp")
	
	labels = [record.timestamp.strftime("%Y-%m-%d") for record in history_records]
	values = [
		float(record.total_value) if record.total_value else 0
		for record in history_records
	]
	
	return render(
		request,
		"reports/history_record_list.html",
		{
			"history_records": history_records,
			"labels": labels,
			"values": values,
			"current_period": period,
		},
	)
