from django import forms

from .models import Reminder


class ReminderForm(forms.ModelForm):
	class Meta:
		model = Reminder
		fields = ["title", "description", "due_at", "severity", "is_active"]
		widgets = {
			"due_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
		}


