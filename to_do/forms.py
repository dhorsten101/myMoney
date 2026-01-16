# forms.py
from django import forms

from to_do.models import ToDo


class ToDoForm(forms.ModelForm):
	class Meta:
		model = ToDo
		fields = [
			"user",
			"name",
			"priority",
		
		]
		widgets = {
			"priority": forms.RadioSelect(attrs={"class": "btn-check"}),
		}
