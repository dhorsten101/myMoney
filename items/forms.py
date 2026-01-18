from django import forms

from items.models import Item, SkuCatalog


class SkuCatalogForm(forms.ModelForm):
	class Meta:
		model = SkuCatalog
		fields = ["sku", "description", "model"]
		widgets = {
			"sku": forms.TextInput(attrs={"class": "form-control"}),
			"description": forms.TextInput(attrs={"class": "form-control"}),
			"model": forms.TextInput(attrs={"class": "form-control"}),
		}


class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ["sku_catalog", "name", "quantity", "notes", "is_active"]
		widgets = {
			"sku_catalog": forms.Select(attrs={"class": "form-select"}),
			"name": forms.TextInput(attrs={"class": "form-control"}),
			"quantity": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
			"notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
			"is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["sku_catalog"].queryset = SkuCatalog.objects.order_by("sku")
		self.fields["sku_catalog"].required = False
		self.fields["sku_catalog"].label = "SKU / Description"

