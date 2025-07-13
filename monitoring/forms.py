# monitoring/forms.py
from django import forms

from .models import MonitoredDevice


class MonitoredDeviceForm(forms.ModelForm):
	class Meta:
		model = MonitoredDevice
		fields = ["ip_address", "hostname"]


class SubnetDiscoveryForm(forms.Form):
	subnet = forms.CharField(label="Subnet", help_text="e.g. 192.168.1.0/24")
