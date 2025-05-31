# forms.py
from django import forms

from .models import Asset, CryptoStats


class CryptoForm(forms.ModelForm):
	class Meta:
		model = CryptoStats
		fields = [
			"total_value",
		]


class AssetForm(forms.ModelForm):
	class Meta:
		model = Asset
		fields = [
			"name",
			"balance",
			"exchange",
			"converted_zar",
		]
