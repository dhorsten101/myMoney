# forms.py
from django import forms

from weight.models import Weight


class WeightForm(forms.ModelForm):
	class Meta:
		model = Weight
		fields = [
			"weight",
		
		]
