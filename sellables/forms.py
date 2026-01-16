# forms.py
from django import forms

from .models import Sellable, SellableImage


class SellableForm(forms.ModelForm):
	class Meta:
		model = Sellable
		fields = ["user", "name", "price", "sold_price", ]


class SellableImageForm(forms.ModelForm):
	class Meta:
		model = SellableImage
		fields = ["image"]
