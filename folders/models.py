# models.py
from django.db import models


class Folder(models.Model):
	name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['name']
	
	def __str__(self):
		return self.name


class StoredFile(models.Model):
	folder = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE)
	file = models.FileField(upload_to='shared_files/%Y/%m/')
	title = models.CharField(max_length=255)
	uploaded_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['-uploaded_at']
	
	def __str__(self):
		return self.title
