from django import forms
from .models import Offer


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            'company', 'project_name','contact_person', 'project_country', 'offer_date', 'valid_until'
        ]
        widgets = {
            'offer_date': forms.DateInput(attrs={'type': 'date'}),
            'valid_until': forms.DateInput(attrs={'type': 'date'}),
        }



class InitializeCounterForm(forms.Form):
    initial_number = forms.IntegerField(label='Initial Offer Number', min_value=1)