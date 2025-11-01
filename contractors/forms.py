from django import forms

from contractors.models import Contractor


class ContractorForm(forms.ModelForm):
	class Meta:
		model = Contractor
		fields = [
			"name",
			"company",
			"service_category",
			"email",
			"phone",
			"notes",
		]
		widgets = {
			"name": forms.TextInput(attrs={"class": "form-control"}),
			"company": forms.TextInput(attrs={"class": "form-control"}),
			"service_category": forms.TextInput(attrs={"class": "form-control"}),
			"email": forms.EmailInput(attrs={"class": "form-control"}),
			"phone": forms.TextInput(attrs={"class": "form-control"}),
			"notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
		}
