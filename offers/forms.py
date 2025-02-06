from django import forms
from .models import Offer

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['company', 'products', 'valid_until', 'discount', 'notes', 'project_name']
        widgets = {
            'valid_until': forms.DateInput(attrs={'type': 'date'}),
            'products': forms.CheckboxSelectMultiple(),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }