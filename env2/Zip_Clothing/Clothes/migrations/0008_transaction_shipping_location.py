# Generated by Django 2.0 on 2018-03-19 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clothes', '0007_auto_20180318_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='Shipping_Location',
            field=models.CharField(default='124 Road Drive', max_length=140),
            preserve_default=False,
        ),
    ]
