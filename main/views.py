import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from main.models import ErrorLog, AuditLog, ExternalServiceLog

logger = logging.getLogger('django')  # uses the 'django' logger from settings


# Register view
def register(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			from django.contrib.auth import login
			
			login(request, user)
			return redirect("home")
	else:
		form = UserCreationForm()
	return render(request, "registration/register.html", {"form": form})


def pricing(request):
	return render(request, 'pricing.html')


def contact_view(request):
	success = False
	if request.method == "POST":
		name = request.POST.get("name")
		email = request.POST.get("email")
		subject = request.POST.get("subject")
		message = request.POST.get("message")
		
		full_message = f"Message from {name} <{email}>:\n\n{message}"
		
		send_mail(
			subject or "Contact Form Submission",
			full_message,
			settings.DEFAULT_FROM_EMAIL,
			[settings.CONTACT_EMAIL],  # Set this in your settings
		)
		success = True
	
	return render(request, "contact.html", {"success": success})


@login_required
def logs(request):
	return render(request, 'logs.html')


@login_required
def error_log_list(request):
	errors = ErrorLog.objects.order_by("-timestamp")
	paginator = Paginator(errors, 100)  # 10 per page
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	return render(request, "error_log_list.html", {"page_obj": page_obj})


@login_required
def audit_log_list(request):
	audits = AuditLog.objects.order_by("-timestamp")
	paginator = Paginator(audits, 100)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	return render(request, "audit_log_list.html", {"page_obj": page_obj})


@login_required
def service_log_list(request):
	service_logs = ExternalServiceLog.objects.order_by("-timestamp")
	paginator = Paginator(service_logs, 100)  # Show 10 logs per page
	
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	
	return render(request, "service_log_list.html", {"page_obj": page_obj})


def test_error_logging(request):
	try:
		1 / 0  # Deliberate error
	except Exception as e:
		logger.error("Test exception for logging", exc_info=True)
	return HttpResponse("Error triggered and logged.")
