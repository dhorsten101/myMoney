from django import forms

from .models import Target


class TargetForm(forms.ModelForm):
	class Meta:
		model = Target
		fields = ['domain_or_ip']
		labels = {
			'domain_or_ip': 'Subnet',
		}
