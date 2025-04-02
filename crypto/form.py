# forms.py
from django import forms

from .models import Crypto


class CryptoForm(forms.ModelForm):
	class Meta:
		model = Crypto
		fields = [
			"name",
			"description",
			"balance",
			"exchange",
			"converted_zar",
			"price",
		]
