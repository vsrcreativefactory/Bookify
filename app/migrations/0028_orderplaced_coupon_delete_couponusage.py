# Generated by Django 5.0 on 2024-04-03 13:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_coupon_couponusage'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.coupon'),
        ),
        migrations.DeleteModel(
            name='CouponUsage',
        ),
    ]
