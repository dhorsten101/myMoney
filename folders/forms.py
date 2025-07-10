from django import forms

from folders.models import Folder, StoredFile


class FolderForm(forms.ModelForm):
	class Meta:
		model = Folder
		fields = ['name']


class FileUploadForm(forms.ModelForm):
	class Meta:
		model = StoredFile
		fields = ['title', 'file']
