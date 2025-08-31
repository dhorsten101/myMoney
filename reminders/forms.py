from django import forms
from django.utils import timezone

from .models import Reminder


class ReminderForm(forms.ModelForm):
	start_at = forms.DateTimeField(
		required=True,
		widget=forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={"type": "datetime-local"}),
		input_formats=["%Y-%m-%dT%H:%M"],
	)
	end_at = forms.DateTimeField(
		required=False,
		widget=forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={"type": "datetime-local"}),
		input_formats=["%Y-%m-%dT%H:%M"],
	)

	class Meta:
		model = Reminder
		fields = ["title", "description", "start_at", "end_at", "severity"]

	def clean(self):
		cleaned = super().clean()
		start = cleaned.get("start_at")
		end = cleaned.get("end_at")
		if start and end and end < start:
			self.add_error("end_at", "End must be after start")
		return cleaned

	def save(self, commit: bool = True) -> Reminder:
		instance: Reminder = super().save(commit=False)
		# Ensure due_at is set (used as point-in-time and for filtering)
		if not instance.due_at:
			instance.due_at = instance.start_at or timezone.now()
		if commit:
			instance.save()
		return instance


