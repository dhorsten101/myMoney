from django import forms

from .models import Camera


class CameraForm(forms.ModelForm):
	class Meta:
		model = Camera
		fields = "__all__"
	
	def clean_rtsp_url(self):
		url = self.cleaned_data["rtsp_url"]
		if not url.startswith("rtsp://"):
			raise forms.ValidationError("RTSP URL must start with rtsp://")
		return url
