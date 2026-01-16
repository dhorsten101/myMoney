# models.py
from django.conf import settings
from django.db import models


class Folder(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="folders", null=True, blank=True)
	name = models.CharField(max_length=255)
	parent = models.ForeignKey('self', null=True, blank=True, related_name='subfolders', on_delete=models.CASCADE)
	
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['name']
	
	def __str__(self):
		return self.full_path()
	
	def full_path(self):
		# e.g. "Main Folder / Subfolder / Sub-subfolder"
		names = []
		folder = self
		while folder:
			names.insert(0, folder.name)
			folder = folder.parent
		return " / ".join(names)
	
	def get_breadcrumbs(self):
		folder = self
		breadcrumbs = []
		while folder:
			breadcrumbs.append(folder)
			folder = folder.parent
		return reversed(breadcrumbs)


class StoredFile(models.Model):
	folder = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stored_files", null=True, blank=True)
	file = models.FileField(upload_to='shared_files/%Y/%m/')
	title = models.CharField(max_length=255)
	uploaded_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['-uploaded_at']
	
	def __str__(self):
		return self.title
