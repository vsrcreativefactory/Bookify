# Generated by Django 5.0 on 2024-03-24 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_payment_orderplaced'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(default='COD', max_length=100),
        ),
    ]