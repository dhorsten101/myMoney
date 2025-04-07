# forms.py
from django import forms

from .models import CryptoStats


class CryptoForm(forms.ModelForm):
	class Meta:
		model = CryptoStats
		fields = [
			"total_value",
		]
