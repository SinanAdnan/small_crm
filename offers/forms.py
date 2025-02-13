from django import forms
from .models import Offer, DeliveryMethod, Stage, OfferProduct
from company.models import Contact
from products.models import Product, Category

class OfferForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, label='Category')

    class Meta:
        model = Offer
        fields = [
            'company', 
            'project_name', 
            'contact_person', 
            'project_country', 
            'offer_date', 
            'valid_until', 
            'delivery_method', 
            'payment_terms', 
            'delivery_time_weeks', 
            'stage',
            'category'
        ]
        widgets = {
            'project_country': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'country'}),
            'offer_date': forms.DateInput(attrs={'type': 'date', 'autocomplete': 'off'}),
            'valid_until': forms.DateInput(attrs={'type': 'date', 'autocomplete': 'off'}),
            'payment_terms': forms.Textarea(attrs={'rows': 3}),
            'delivery_time_weeks': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'stage': forms.Select(attrs={'class': 'form-control'}),
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

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['name']

class InitializeCounterForm(forms.Form):
    initial_number = forms.IntegerField(label='Initial Offer Number', min_value=1, widget=forms.NumberInput(attrs={'autocomplete': 'off'}))

class OfferProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label="Select a product", required=True)

    class Meta:
        model = OfferProduct
        fields = [
            'product', 'product_code', 'product_name', 'size', 'material', 'unit_cost', 'margin', 'price', 'discount_percentage', 'description', 'quantity'
        ]
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'product_code': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'material': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'margin': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)
        if product_id:
            product = Product.objects.get(id=product_id)
            self.fields['product_code'].initial = product.product_code
            self.fields['product_name'].initial = product.name
            self.fields['size'].initial = product.size
            self.fields['material'].initial = product.material
            self.fields['unit_cost'].initial = product.unit_cost
            self.fields['margin'].initial = product.margin
            self.fields['price'].initial = product.price
            self.fields['description'].initial = product.description