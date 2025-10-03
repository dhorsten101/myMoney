from django import forms

from invoicing.models import Invoice, RentalProperty, RentalPropertyImage, RentalPropertyPipeline, MonthlyExpense, RentalAgent, EstateAgent, ManagingAgent, RentalPropertyPipelineImage


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
			"total",  # capture Gross Total (incl. VAT) directly
			"notes",
		]
		widgets = {
			"issue_date": forms.DateInput(attrs={"type": "date"}),
			"due_date": forms.DateInput(attrs={"type": "date"}),
		}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Relabel total field
		self.fields["total"].label = "Total (incl. VAT)"

	def clean(self):
		cleaned = super().clean()
		return cleaned

	def save(self, commit=True):
		"""
		Treat the entered "total" field as Gross Total (incl. VAT at 15%).
		Back-calculate net (subtotal field in DB) and tax so that:
			total = entered_amount
			tax = round(net * 0.15, 2)
			net = total / 1.15
		"""
		instance = super().save(commit=False)
		try:
			from decimal import Decimal, ROUND_HALF_UP
			entered_total = self.cleaned_data.get("total") or Decimal("0")
			if entered_total < 0:
				entered_total = Decimal("0")
			# Compute net by dividing by 1.15 and rounding to cents
			net = (entered_total / Decimal("1.15")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
			tax = (net * Decimal("0.15")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
			instance.subtotal = net
			instance.tax = tax
			instance.total = (net + tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
		except Exception:
			# Fallback to default model behavior if anything unexpected occurs
			pass
		if commit:
			instance.save()
		return instance


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
			"estate_agent",
			"managing_agent",
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
			"estate_agent": forms.Select(attrs={"class": "form-select"}),
			"managing_agent": forms.Select(attrs={"class": "form-select"}),
		}


class RentalPropertyImageForm(forms.ModelForm):
	class Meta:
		model = RentalPropertyImage
		fields = ["image"]
		widgets = {
			"image": forms.ClearableFileInput(attrs={"class": "form-control"}),
		}


class RentalPropertyPipelineImageForm(forms.ModelForm):
	class Meta:
		model = RentalPropertyPipelineImage
		fields = ["image"]
		widgets = {
			"image": forms.ClearableFileInput(attrs={"class": "form-control"}),
		}


class RentalPropertyPipelineForm(forms.ModelForm):
	class Meta:
		model = RentalPropertyPipeline
		fields = ["url", "title", "notes", "price"]
		widgets = {
			"url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://..."}),
			"title": forms.TextInput(attrs={"class": "form-control"}),
			"notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
			"price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
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


class EstateAgentForm(forms.ModelForm):
	class Meta:
		model = EstateAgent
		fields = ["name", "email", "phone", "notes"]
		widgets = {
			"name": forms.TextInput(attrs={"class": "form-control"}),
			"email": forms.EmailInput(attrs={"class": "form-control"}),
			"phone": forms.TextInput(attrs={"class": "form-control"}),
			"notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
		}


class ManagingAgentForm(forms.ModelForm):
	class Meta:
		model = ManagingAgent
		fields = ["name", "email", "phone", "notes"]
		widgets = {
			"name": forms.TextInput(attrs={"class": "form-control"}),
			"email": forms.EmailInput(attrs={"class": "form-control"}),
			"phone": forms.TextInput(attrs={"class": "form-control"}),
			"notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
		}


class RentalPropertyManagingAgentForm(forms.ModelForm):
	class Meta:
		model = RentalProperty
		fields = ["managing_agent"]
		widgets = {
			"managing_agent": forms.Select(attrs={"class": "form-select"}),
		}
