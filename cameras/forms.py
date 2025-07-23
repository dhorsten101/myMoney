from django import forms

from .models import Camera


class CameraForm(forms.ModelForm):
	class Meta:
		model = Camera
		fields = [
			"name", "location", "ip_address", "rtsp_url",
			"stream_slug", "username", "password"
		]
		widgets = {
			"password": forms.PasswordInput(render_value=True),
		}
