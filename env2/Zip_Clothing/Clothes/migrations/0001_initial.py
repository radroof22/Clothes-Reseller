# Generated by Django 2.0 on 2017-12-24 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=500)),
                ('Image', models.ImageField(upload_to='')),
                ('DateTime', models.DateTimeField(auto_now_add=True)),
                ('Price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('_Bought', models.BooleanField(default=False)),
                ('Seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
