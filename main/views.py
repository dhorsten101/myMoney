from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.shortcuts import render


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
