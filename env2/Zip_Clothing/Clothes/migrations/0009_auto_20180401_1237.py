# Generated by Django 2.0 on 2018-04-01 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clothes', '0008_transaction_shipping_location'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.AddField(
            model_name='transaction',
            name='PP_Id',
            field=models.CharField(default=1234, max_length=30),
            preserve_default=False,
        ),
    ]