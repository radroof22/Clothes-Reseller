# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-16 23:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clothes', '0009_payment_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothing_purchase',
            name='Address',
            field=models.CharField(default='312 Basker Dr. Philly, PA', max_length=140),
            preserve_default=False,
        ),
    ]
