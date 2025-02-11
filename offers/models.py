from django.db import models
from company.models import Company, Contact
from django_countries.fields import CountryField

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

    def save(self, *args, **kwargs):
        if not self.pk:
            counter, _ = OfferCounter.objects.get_or_create(pk=1)
            self.offer_number = counter.increment()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Offer {self.offer_number} for {self.project_name} to {self.company.name} valid until {self.valid_until}"