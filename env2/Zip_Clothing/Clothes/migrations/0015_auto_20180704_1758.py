# Generated by Django 2.0 on 2018-07-04 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clothes', '0014_auto_20180703_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='Votes',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='Size',
        ),
        migrations.AddField(
            model_name='product',
            name='Size',
            field=models.CharField(default='M', max_length=50),
            preserve_default=False,
        ),
    ]