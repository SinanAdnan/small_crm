from django.db import models
from django_countries.fields import CountryField
from django.urls import reverse


class Company(models.Model):

    
    CLASSIFICATION_CHOICES = [
        ('High Value', 'High Value'),
        ('Medium Value', 'Medium Value'),
        ('Low Value', 'Low Value'),
        ('Unimportant', 'Unimportant'),
    ]

    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField()
    city = models.CharField(max_length=100, null=True, blank=True)
    country = CountryField(blank_label='(Select a country)', null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    classification = models.CharField(
        max_length=15,
        choices=CLASSIFICATION_CHOICES,
        default='Unimportant'
    )
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('company_detail', args=[str(self.id)])

class Contact(models.Model):
    company = models.ForeignKey('Company', related_name='contacts', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100, blank=True, null=True)  # Optional field
    position = models.CharField(max_length=100, blank=True, null=True)  # Optional field
    country = CountryField(blank_label='(Select a country)', null=True, blank=True)  # Optional field
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    image = models.ImageField(
        upload_to='contact_images/', 
        default='contact_images/default_user.png'
        )
    linkedin_profile = models.URLField(max_length=200, blank=True, null=True)
    preferred_communication = models.CharField(
        max_length=50,
        choices=[
            ('Email', 'Email'),
            ('Phone', 'Phone'),
            ('In-person', 'In-person'),
            ('Messaging', 'Messaging'),
        ],
        blank=True,
        null=True
    )
    behavior = models.TextField(blank=True, null=True)  # For notes on behavior
    
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.second_name if self.second_name else ''} {self.position if self.position else ''}"

    def get_absolute_url(self):
        return reverse('contact_detail', args=[str(self.id)])