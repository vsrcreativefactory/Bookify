# Generated by Django 5.0 on 2024-03-15 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_remove_customer_email_remove_customer_otp_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]