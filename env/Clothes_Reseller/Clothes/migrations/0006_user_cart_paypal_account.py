# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-07 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clothes', '0005_auto_20171027_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_cart',
            name='Paypal_Account',
            field=models.CharField(default=549549549549, max_length=16),
            preserve_default=False,
        ),
    ]
