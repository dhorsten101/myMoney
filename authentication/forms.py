from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
	"""
	UserCreationForm bound to the swapped AUTH_USER_MODEL (email-based).
	"""

	class Meta(UserCreationForm.Meta):
		model = User
		fields = ("email",)
		widgets = {
			"email": forms.EmailInput(attrs={"class": "form-control"}),
		}

