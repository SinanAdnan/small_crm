from django import forms
from .models import Company, Contact

class CompanyForm(forms.ModelForm):
    
    class Meta:
        model = Company
        fields = ['name', 'logo', 'description', 'address', 'city', 'country', 'phone', 'email', 'website', 'classification']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Company Description'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Company Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website URL'}),
            
        }
class ContactForm(forms.ModelForm):
    
    class Meta:
        model = Contact
        fields = ['first_name', 'second_name', 'position', 'country', 'phone', 'email' , 'image' ,
            'linkedin_profile', 'preferred_communication', 'behavior',
             'additional_info']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Second Name'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'behavior': forms.Textarea(attrs={'rows': 3}),
            'additional_info': forms.Textarea(attrs={'rows': 3}),
        }