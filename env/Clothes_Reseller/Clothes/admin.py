from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Clothing_Post)
admin.site.register(models.Clothing_Purchase)
admin.site.register(models.Cart_Item)
admin.site.register(models.User_Cart)
admin.site.register(models.Payment)