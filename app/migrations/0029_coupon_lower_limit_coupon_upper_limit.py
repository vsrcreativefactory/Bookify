# Generated by Django 5.0 on 2024-04-03 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_orderplaced_coupon_delete_couponusage'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='lower_limit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='coupon',
            name='upper_limit',
            field=models.DecimalField(decimal_places=2, default=10000, max_digits=8),
        ),
    ]
