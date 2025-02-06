# Generated by Django 4.2.4 on 2025-02-04 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='production_time',
            field=models.PositiveIntegerField(default=8, help_text='Estimated production time in days'),
            preserve_default=False,
        ),
    ]
