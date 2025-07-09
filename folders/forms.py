from django import forms


class FolderForm(forms.ModelForm):
	class Meta:
		model = Folder
		fields = ['name']


class FileUploadForm(forms.ModelForm):
	class Meta:
		model = StoredFile
		fields = ['title', 'file']
