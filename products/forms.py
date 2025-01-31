# products/forms.py
from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'product_code', 'category', 'model', 'size', 
            'unit_cost', 'margin', 'images', 'technical_specification', 
            'material', 'description', 'warranty_information'
        ]
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
        }