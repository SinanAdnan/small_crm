# products/forms.py
from django import forms
from .models import Product, Category

Category.objects.create(name='Electronics')
Category.objects.create(name='Furniture')
Category.objects.create(name='Apparel')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'product_code', 'category', 'model', 'size', 
            'unit_cost', 'margin', 'images', 'technical_specification', 
            'material', 'description', 'warranty_information'
        ]
    
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category")
