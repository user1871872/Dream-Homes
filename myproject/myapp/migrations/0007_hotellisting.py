# Generated by Django 5.0.2 on 2024-02-21 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_remove_customuser_approved_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available_for_sale', models.BooleanField(default=False)),
                ('available_for_rent', models.BooleanField(default=False)),
                ('contact_email', models.EmailField(max_length=254)),
            ],
        ),
    ]
