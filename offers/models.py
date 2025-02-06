from django.db import models
from company.models import Company
from products.models import Product

class Offer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    offer_date = models.DateField(auto_now_add=True)
    valid_until = models.DateField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    offer_number = models.PositiveIntegerField(unique=True)
    project_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.pk:
            last_offer = Offer.objects.order_by('-offer_number').first()
            self.offer_number = (last_offer.offer_number + 1) if last_offer else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Offer {self.offer_number} - {self.project_name} to {self.company.name} valid until {self.valid_until}"