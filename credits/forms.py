# forms.py
from django import forms

from .models import Credit


class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = [
            "name",
            "description",
            "balance",
        ]
