# Generated by Django 5.0 on 2024-03-13 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_customer_otp_remove_customer_uid_emailuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='User',
            new_name='user',
        ),
    ]