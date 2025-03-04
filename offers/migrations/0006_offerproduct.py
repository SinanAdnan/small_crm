# Generated by Django 5.1.5 on 2025-02-12 10:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0005_stage_offer_stage'),
        ('products', '0003_alter_product_production_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(max_length=100)),
                ('product_name', models.CharField(max_length=200)),
                ('size', models.CharField(max_length=50)),
                ('material', models.CharField(max_length=200)),
                ('unit_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('margin', models.DecimalField(decimal_places=2, max_digits=5)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_percentage', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('description', models.TextField()),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_products', to='offers.offer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
