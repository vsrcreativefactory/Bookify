# Generated by Django 5.0 on 2024-03-24 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_payment_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
