# Generated by Django 5.1.5 on 2025-02-11 09:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0002_alter_offer_project_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='offer',
            name='payment_terms',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='delivery_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='offers.deliverymethod'),
        ),
    ]
