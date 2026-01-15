from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission


User = get_user_model()


class UserAdminEditForm(forms.ModelForm):
	groups = forms.ModelMultipleChoiceField(
		queryset=Group.objects.all(),
		required=False,
		widget=forms.SelectMultiple(attrs={"class": "form-select"}),
	)

	class Meta:
		model = User
		fields = ["email", "is_active", "is_staff", "is_superuser", "groups"]
		widgets = {
			"email": forms.EmailInput(attrs={"class": "form-control"}),
			"is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
			"is_staff": forms.CheckboxInput(attrs={"class": "form-check-input"}),
			"is_superuser": forms.CheckboxInput(attrs={"class": "form-check-input"}),
		}


class GroupAdminForm(forms.ModelForm):
	permissions = forms.ModelMultipleChoiceField(
		queryset=Permission.objects.select_related("content_type").order_by("content_type__app_label", "codename"),
		required=False,
		widget=forms.SelectMultiple(attrs={"class": "form-select", "size": "12"}),
	)

	class Meta:
		model = Group
		fields = ["name", "permissions"]
		widgets = {
			"name": forms.TextInput(attrs={"class": "form-control"}),
		}

