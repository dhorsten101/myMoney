from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import AttendanceRecord, AttendanceEntry


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
	today = timezone.localdate()
	record, _ = AttendanceRecord.objects.get_or_create(user=request.user, date=today)
	open_entry = record.entries.filter(end_time__isnull=True).first()
	recent_records = AttendanceRecord.objects.filter(user=request.user).order_by("-date")[:30]
	context = {
		"record": record,
		"open_entry": open_entry,
		"recent_records": recent_records,
		"now": timezone.now(),
	}
	return render(request, "dashboard.html", context)


@login_required
def check_in(request: HttpRequest) -> HttpResponse:
	if request.method != "POST":
		return HttpResponseBadRequest("Invalid method")
	
	today = timezone.localdate()
	record, _ = AttendanceRecord.objects.get_or_create(user=request.user, date=today)
	
	# only create a new entry if no open one exists
	if not record.entries.filter(end_time__isnull=True).exists():
		AttendanceEntry.objects.create(record=record, start_time=timezone.now())
	
	return redirect("time_tracker:dashboard")


@login_required
def check_out(request: HttpRequest) -> HttpResponse:
	if request.method != "POST":
		return HttpResponseBadRequest("Invalid method")
	
	today = timezone.localdate()
	try:
		record = AttendanceRecord.objects.get(user=request.user, date=today)
	except AttendanceRecord.DoesNotExist:
		return redirect("time_tracker:dashboard")


def _is_staff(user) -> bool:
	return user.is_authenticated and user.is_staff


@user_passes_test(_is_staff)
def overview(request: HttpRequest) -> HttpResponse:
	# Optional date filtering via ?date=YYYY-MM-DD
	date_str = request.GET.get("date")
	if date_str:
		try:
			target_date = timezone.datetime.fromisoformat(date_str).date()
		except Exception:
			target_date = timezone.localdate()
	else:
		target_date = timezone.localdate()
	
	records = (
		AttendanceRecord.objects
		.filter(date=target_date)
		.select_related("user")
		.prefetch_related("entries")
		.order_by("user__username")
	)
	
	context = {
		"target_date": target_date,
		"records": records,
	}
	return render(request, "time_tracker/overview.html", context)
