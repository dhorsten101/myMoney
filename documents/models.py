# models.py
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

CATEGORY_CHOICES = [
	("personal", "Personal"),
	("work", "Work"),
	("finance", "Finance"),
	("legal", "Legal"),
	("other", "Other"),
]


class Document(models.Model):
	title = models.CharField(max_length=255)
	content = CKEditor5Field('Content', config_name='default')
	category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="personal")
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.title
