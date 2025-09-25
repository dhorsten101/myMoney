from django import forms

from invoicing.models import Invoice, RentalProperty


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
            "capital_value",
            "flow_value",
            "cost_value",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "capital_value": forms.NumberInput(attrs={"class": "form-control"}),
            "flow_value": forms.NumberInput(attrs={"class": "form-control"}),
            "cost_value": forms.NumberInput(attrs={"class": "form-control"}),
        }


