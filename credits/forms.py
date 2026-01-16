# forms.py
from django import forms

from .models import Credit


class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = [
            "user",
            "name",
            "description",
            "balance",
        ]
