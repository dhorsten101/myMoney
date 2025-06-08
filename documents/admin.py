from django import forms
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Document


class DocumentAdminForm(forms.ModelForm):
	class Meta:
		model = Document
		fields = '__all__'
		widgets = {
			'content': CKEditor5Widget(config_name='default')
		}


class DocumentAdmin(admin.ModelAdmin):
	form = DocumentAdminForm


admin.site.register(Document, DocumentAdmin)
