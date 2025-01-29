# products/models.py
from django.db import models
from math import ceil

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    product_code = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    margin = models.DecimalField(max_digits=5, decimal_places=2, default=30)  # Default margin is 30%
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    images = models.ImageField(upload_to='products/', blank=True, null=True)
    technical_specification = models.FileField(upload_to='product_specs/', blank=True, null=True)
    material = models.CharField(max_length=200)
    description = models.TextField()
    warranty_information = models.TextField()

    def save(self, *args, **kwargs):
        if self.product_code:
            self.product_code = self.product_code.upper()
           
        # Calculate the price based on the unit cost and margin
        self.price = ceil(self.unit_cost / (1 - (self.margin/100)))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
