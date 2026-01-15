from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import ModelForm

from .models import User


class UserCreationForm(ModelForm):
	class Meta:
		model = User
		fields = ("email",)


class UserChangeForm(ModelForm):
	class Meta:
		model = User
		fields = "__all__"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm
	
	model = User
	
	list_display = (
		"email",
		"is_staff",
		"is_superuser",
		"is_active",
	)
	list_filter = (
		"is_staff",
		"is_superuser",
		"is_active",
	)
	
	search_fields = ("email",)
	ordering = ("email",)
	filter_horizontal = ("groups", "user_permissions")
	
	fieldsets = (
		(None, {"fields": ("email", "password")}),
		(
			"Permissions",
			{
				"fields": (
					"is_active",
					"is_staff",
					"is_superuser",
					"groups",
					"user_permissions",
				)
			},
		),
	)
	
	add_fieldsets = (
		(
			None,
			{
				"classes": ("wide",),
				"fields": (
					"email",
					"password1",
					"password2",
					"is_staff",
					"is_superuser",
					"is_active",
				),
			},
		),
	)
