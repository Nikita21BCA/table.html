from django import forms
from .models import LedgerEntry

class LedgerForm(forms.ModelForm):
    class Meta:
        model = LedgerEntry
        fields = '__all__'
