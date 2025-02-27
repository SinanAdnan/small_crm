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
    yearly_target = models.DecimalField(max_digits=10, decimal_places=2, default=1200000)
    active_line = models.DecimalField(max_digits=10, decimal_places=2, default=1560000)  # 30% more than target
    poor_line = models.DecimalField(max_digits=10, decimal_places=2, default=720000)  # 40% less than target
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('company_detail', args=[str(self.id)])

class Contact(models.Model):
    company = models.ForeignKey('Company', related_name='contacts', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(blank_label='(Select a country)', null=True, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "A contact with this email already exists.",
        }
    )
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
        null=True,
        default='Email'
    )
    behavior = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.second_name if self.second_name else ''} {self.position if self.position else ''}"

    def get_absolute_url(self):
        return reverse('contact_detail', args=[str(self.id)])