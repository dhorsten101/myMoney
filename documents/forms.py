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
