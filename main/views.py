# views.py
import logging

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from authentication.forms import CustomUserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from api.models import Quote
from credits.models import Credit
from cryptos.models import Asset
from documents.models import Document
from expenses.models import Expense
from history_records.models import HistoryRecord
from ideas.models import Idea
from incomes.models import Income
from main.models import ErrorLog, AuditLog, ExternalServiceLog
from sellables.models import Sellable
from to_do.models import ToDo
from weight.models import Weight
from worth.models import Worth

logger = logging.getLogger('django')  # uses the 'django' logger from settings


class SimplePasswordResetForm(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
	new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
	new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

	def clean(self):
		cleaned = super().clean()
		p1 = cleaned.get("new_password1")
		p2 = cleaned.get("new_password2")
		if p1 and p2 and p1 != p2:
			raise forms.ValidationError("Passwords do not match.")
		if p1:
			validate_password(p1)
		return cleaned


def password_reset(request):
	"""
	Simple in-app reset: email + new password. No email links, no messages.
	Always redirects back to login on success (or if user is not found).
	"""
	if request.method == "POST":
		form = SimplePasswordResetForm(request.POST)
		if form.is_valid():
			User = get_user_model()
			email = form.cleaned_data["email"].strip()
			new_password = form.cleaned_data["new_password1"]
			try:
				user = User.objects.get(email__iexact=email)
				user.set_password(new_password)
				user.save(update_fields=["password"])
			except User.DoesNotExist:
				pass
			return redirect("login")
	else:
		form = SimplePasswordResetForm()
	return render(request, "registration/password_reset_form.html", {"form": form})


# Register view
def register(request):
	if request.method == "POST":
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			from django.contrib.auth import login
			
			login(request, user)
			return redirect("home")
	else:
		form = CustomUserCreationForm()
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
	paginator = Paginator(errors, 50)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	return render(request, "error_log_list.html", {"page_obj": page_obj})


@login_required
def audit_log_list(request):
	audits = AuditLog.objects.order_by("-timestamp")
	paginator = Paginator(audits, 50)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	return render(request, "audit_log_list.html", {"page_obj": page_obj})


@login_required
def service_log_list(request):
	service_logs = ExternalServiceLog.objects.order_by("-timestamp")
	paginator = Paginator(service_logs, 50)  # Show 50 logs per page
	
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	
	return render(request, "service_log_list.html", {"page_obj": page_obj})


def test_error_logging(request):
	try:
		1 / 0  # Deliberate error
	except Exception as e:
		logger.error("Test exception for logging", exc_info=True)
	return HttpResponse("Error triggered and logged.")


def global_search(request):
	query = request.GET.get("q", "")
	results = {}
	has_results = False
	
	if query:
		results = {
			"documents": Document.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)),
			"todos": ToDo.objects.filter(Q(name__icontains=query)),
			"ideas": Idea.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)),
			"quotes": Quote.objects.filter(Q(text__icontains=query) | Q(author__icontains=query)),
			"worth": Worth.objects.filter(Q(name__icontains=query) | Q(notes__icontains=query)),
			"credits": Credit.objects.filter(Q(name__icontains=query)),
			"expenses": Expense.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)),
			"incomes": Income.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)),
			"sellables": Sellable.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)),
			"weights": Weight.objects.filter(Q(weight__icontains=query)),
			"history": HistoryRecord.objects.filter(Q(total_value__icontains=query)),
			"assets": Asset.objects.filter(Q(name__icontains=query) | Q(exchange__icontains=query)),
		}
		# Determine if any results exist without forcing full evaluation
		has_results = any(qs.exists() for qs in results.values())

	return render(request, "components/global_search.html", {"query": query, "results": results, "has_results": has_results})


def uml_view(request):
	return render(request, 'uml_view.html', {})


def home(request):
    # Optional context: show quote if available
    from api.models import Quote
    quote = Quote.objects.order_by('-id').first()
    return render(request, 'home.html', {"quote": quote})
