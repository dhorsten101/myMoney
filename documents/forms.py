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
		('floorplan', 'Floorplan'),
		('legal', 'Legal'),
		('finance', 'Finance'),
	]
	category = forms.ChoiceField(choices=CATEGORY_CHOICES)

	class Meta:
		model = Document
		fields = ['title', 'category', 'file', 'description']
