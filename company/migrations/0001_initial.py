# Generated by Django 5.1.5 on 2025-01-20 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('website', models.URLField()),
            ],
        ),
    ]
