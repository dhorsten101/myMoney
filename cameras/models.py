from django.db import models


class Camera(models.Model):
	name = models.CharField(max_length=100)
	location = models.CharField(max_length=255, blank=True)
	rtsp_url = models.URLField()
	stream_slug = models.SlugField(unique=True)
	ip_address = models.GenericIPAddressField()
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.name
