from django.db import models
from company.models import Company, Contact
from django_countries.fields import CountryField
from products.models import Product, Category

class DeliveryMethod(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class OfferCounter(models.Model):
    base_number = models.PositiveIntegerField(default=11000)
    current_number = models.PositiveIntegerField(default=11000)

    def increment(self):
        self.current_number += 1
        self.save()
        return self.current_number

    def __str__(self):
        return f"Current Offer Number: {self.current_number}"

class Stage(models.Model):
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def previous_stage(self):
        previous_stages = Stage.objects.filter(pk__lt=self.pk).order_by('-pk')
        if previous_stages.exists():
            return previous_stages.first()
        return None

    def delete(self, *args, **kwargs):
        previous_stage = self.previous_stage()
        if previous_stage:
            Offer.objects.filter(stage=self).update(stage=previous_stage)
        else:
            Offer.objects.filter(stage=self).update(stage=None)
        super().delete(*args, **kwargs)

class OfferProduct(models.Model):
    offer = models.ForeignKey('Offer', on_delete=models.CASCADE, related_name='offer_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_code = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    size = models.CharField(max_length=50)
    material = models.CharField(max_length=200)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    margin = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    description = models.TextField()
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        if not self.product_code:
            self.product_code = self.product.product_code
        if not self.product_name:
            self.product_name = self.product.name
        if not self.size:
            self.size = self.product.size
        if not self.material:
            self.material = self.product.material
        if not self.unit_cost:
            self.unit_cost = self.product.unit_cost
        if not self.margin:
            self.margin = self.product.margin
        if not self.price:
            self.price = self.product.price
        if not self.description:
            self.description = self.product.description
        super().save(*args, **kwargs)

class Offer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact_person = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.SET_NULL, null=True, blank=True)
    offer_number = models.PositiveIntegerField(unique=True)
    offer_date = models.DateField(auto_now_add=False, default=None)
    valid_until = models.DateField()
    notes = models.TextField(blank=True, null=True)
    project_name = models.CharField(max_length=255)
    project_country = CountryField(blank_label='(Select a country)', null=True, blank=True)
    payment_terms = models.TextField(blank=True, null=True)
    delivery_time_weeks = models.PositiveIntegerField(null=True, blank=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 

    def save(self, *args, **kwargs):
        if not self.pk:
            counter, _ = OfferCounter.objects.get_or_create(pk=1)
            self.offer_number = counter.increment()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Offer {self.offer_number} for {self.project_name} to {self.company.name} valid until {self.valid_until}"
    
    @property
    def total_amount(self):
        return sum(product.total_price() for product in self.offer_products.all())