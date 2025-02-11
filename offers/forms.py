from django import forms
from .models import Offer, DeliveryMethod
from company.models import Contact

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            'company', 'project_name', 'contact_person', 'project_country', 'offer_date', 'valid_until', 'delivery_method', 'payment_terms'
        ]
        widgets = {
            'project_country': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'country'}),
            'offer_date': forms.DateInput(attrs={'type': 'date', 'autocomplete': 'off'}),
            'valid_until': forms.DateInput(attrs={'type': 'date', 'autocomplete': 'off'}),
            'payment_terms': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact_person'].queryset = Contact.objects.none()
        self.fields['company'].widget.attrs.update({'autocomplete': 'organization'})
        self.fields['project_name'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['contact_person'].widget.attrs.update({'autocomplete': 'name'})

        if 'company' in self.data:
            try:
                company_id = int(self.data.get('company'))
                self.fields['contact_person'].queryset = Contact.objects.filter(company_id=company_id).order_by('first_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Contact queryset
        elif self.instance.pk:
            self.fields['contact_person'].queryset = self.instance.company.contacts.order_by('first_name')

class DeliveryMethodForm(forms.ModelForm):
    class Meta:
        model = DeliveryMethod
        fields = ['name', 'description']

class InitializeCounterForm(forms.Form):
    initial_number = forms.IntegerField(label='Initial Offer Number', min_value=1, widget=forms.NumberInput(attrs={'autocomplete': 'off'}))