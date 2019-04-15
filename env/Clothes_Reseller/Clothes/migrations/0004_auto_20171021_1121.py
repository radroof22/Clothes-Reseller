# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-21 15:21
from __future__ import unicode_literals

import Clothes.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Clothes', '0003_clothing_post_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clothing_Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateTime_Purchased', models.DateTimeField()),
                ('Delivered', models.BooleanField()),
                ('Buyer', models.ForeignKey(on_delete=models.SET(Clothes.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='clothing_post',
            name='Bought',
        ),
        migrations.AddField(
            model_name='clothing_purchase',
            name='Clothing_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Clothes.Clothing_Post'),
        ),
    ]
