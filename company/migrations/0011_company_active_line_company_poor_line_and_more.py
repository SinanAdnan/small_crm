# Generated by Django 5.1.5 on 2025-02-19 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_company_created_at_company_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='active_line',
            field=models.DecimalField(decimal_places=2, default=1560000, max_digits=10),
        ),
        migrations.AddField(
            model_name='company',
            name='poor_line',
            field=models.DecimalField(decimal_places=2, default=720000, max_digits=10),
        ),
        migrations.AddField(
            model_name='company',
            name='yearly_target',
            field=models.DecimalField(decimal_places=2, default=1200000, max_digits=10),
        ),
    ]
