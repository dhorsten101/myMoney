from django.db import models


class Camera(models.Model):
	name = models.CharField(max_length=100)
	location = models.CharField(max_length=255, blank=True)
	rtsp_url = models.URLField()
	stream_slug = models.SlugField(unique=True)  # used for HLS directory name
	
	def __str__(self):
		return self.name
