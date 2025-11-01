from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Document


class DocumentForm(forms.ModelForm):
	class Meta:
		model = Document
		fields = ['title', 'category', 'content']
		widgets = {
			'content': CKEditor5Widget(config_name='default'),
		}


class DocumentUploadForm(forms.ModelForm):
	# Restrict category choices for door uploads per requirement
	CATEGORY_CHOICES = [
		('expense', 'Expense'),
		('invoice', 'Invoice'),
		('finance', 'Finance'),
		('legal', 'Legal'),
		('floorplan', 'Floorplan'),
		('leases', 'Leases'),
		('deeds', 'Deeds'),
	]
	category = forms.ChoiceField(choices=CATEGORY_CHOICES)
	create_as = forms.ChoiceField(
		choices=[
			('none', 'Just Upload (no analysis)'),
			('expense', 'Create Expense'),
			('invoice', 'Create Invoice'),
		],
		initial='none',
		required=False,
	)

	class Meta:
		model = Document
		fields = ['title', 'category', 'file', 'description']
