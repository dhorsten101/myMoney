# forms.py
from django import forms

from .models import Worth


class WorthForm(forms.ModelForm):
	class Meta:
		model = Worth
		fields = [
			"name",
			# "notes",
			"quick_value",
			"real_value",
			"category",
		]
