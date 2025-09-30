from django import forms

from invoicing.models import Invoice, RentalProperty, RentalPropertyImage, RentalPropertyPipeline, MonthlyExpense, RentalAgent


class InvoiceForm(forms.ModelForm):
	class Meta:
		model = Invoice
		fields = [
			"customer_name",
			"customer_email",
			"issue_date",
			"due_date",
			"status",
			"rental_property",
			"subtotal",
			"notes",
		]
		widgets = {
			"issue_date": forms.DateInput(attrs={"type": "date"}),
			"due_date": forms.DateInput(attrs={"type": "date"}),
		}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Tax is computed; show as read-only if present in bound instance
		# Optionally, we could add a non-editable display, but we keep the form clean


class RentalPropertyForm(forms.ModelForm):
	class Meta:
		model = RentalProperty
		fields = [
			"name",
			"address",
			"website",
			"capital_value",
			"flow_value",
			"levies",
			"rates_taxes",
			"water_electricity",
			"internet",
			"agent",
		]
		widgets = {
			"name": forms.TextInput(attrs={"class": "form-control"}),
			"address": forms.TextInput(attrs={"class": "form-control"}),
			"website": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://..."}),
			"capital_value": forms.NumberInput(attrs={"class": "form-control"}),
			"flow_value": forms.NumberInput(attrs={"class": "form-control"}),
			"levies": forms.NumberInput(attrs={"class": "form-control"}),
			"rates_taxes": forms.NumberInput(attrs={"class": "form-control"}),
			"water_electricity": forms.NumberInput(attrs={"class": "form-control"}),
			"internet": forms.NumberInput(attrs={"class": "form-control"}),
			"agent": forms.Select(attrs={"class": "form-select"}),
		}


class RentalPropertyImageForm(forms.ModelForm):
	class Meta:
		model = RentalPropertyImage
		fields = ["image"]
		widgets = {
			"image": forms.ClearableFileInput(attrs={"class": "form-control"}),
		}


class RentalPropertyPipelineForm(forms.ModelForm):
	class Meta:
		model = RentalPropertyPipeline
		fields = ["url", "title", "notes"]
		widgets = {
			"url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://..."}),
			"title": forms.TextInput(attrs={"class": "form-control"}),
			"notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
		}


class MonthlyExpenseForm(forms.ModelForm):
	class Meta:
		model = MonthlyExpense
		fields = ["date", "amount", "description", "property"]
		widgets = {
			"date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
			"amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
			"description": forms.TextInput(attrs={"class": "form-control"}),
			"property": forms.Select(attrs={"class": "form-select"}),
		}


class RentalAgentForm(forms.ModelForm):
	class Meta:
		model = RentalAgent
		fields = ["name", "email", "phone", "notes"]
		widgets = {
			"name": forms.TextInput(attrs={"class": "form-control"}),
			"email": forms.EmailInput(attrs={"class": "form-control"}),
			"phone": forms.TextInput(attrs={"class": "form-control"}),
			"notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
		}
