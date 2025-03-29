# forms.py
from django import forms

from .models import Idea


class IdeaForm(forms.ModelForm):
	class Meta:
		model = Idea
		fields = ["name", "description"]

# class SellableImageForm(forms.ModelForm):
# 	class Meta:
# 		model = SellableImage
# 		fields = ["image"]
