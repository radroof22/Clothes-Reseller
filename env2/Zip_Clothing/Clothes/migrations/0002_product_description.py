# Generated by Django 2.0 on 2017-12-24 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clothes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Description',
            field=models.TextField(default="This is a very noice product. Very high quality and I didn't even use it that often!"),
            preserve_default=False,
        ),
    ]
