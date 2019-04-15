from django.db import models
from django.contrib.auth import models as auth_models
from django.shortcuts import redirect


# Create your models here.

## Products
class Product(models.Model):
    Name = models.CharField(max_length=500)
    Description = models.TextField()
    Seller = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    Image = models.ImageField(upload_to="Product/")
    DateTime = models.DateTimeField(auto_now_add=True)
    Price = models.DecimalField(max_digits = 7,decimal_places=2)
    Bought = models.BooleanField(default=False)
    Size = models.CharField(max_length=50)

    def __str__(self):
        return "{}-{}: ({})".format(self.Name, self.Seller,self.DateTime)

    def get_url(self):
        return redirect("Detail_Product", prod_id=self.id)

    def get_date(self):
        return "{}/{}/{} at {}:{}".format(self.DateTime.month,self.DateTime.day,self.DateTime.year,self.DateTime.hour,self.DateTime.minute)
    
## Buying
class Transaction(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Buyer = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    Shipping_Location = models.CharField(max_length=140)
    DateTime = models.DateTimeField(auto_now_add=True)
    Shipped = models.BooleanField(default=False)
    Shipping_Receipt = models.ImageField(blank=True, null=True)
    Complete = models.BooleanField(default=False)
    


    def __str__(self):
        return "{}:{}".format(self.Product, self.Buyer)

    def get_date(self):
        return "{}/{}/{} at {}:{}".format(self.DateTime.month,self.DateTime.day,self.DateTime.year,self.DateTime.hour,self.DateTime.minute)


def get_Transaction_by_Product_or_None(in_product):
    transactions = Transaction.objects.all()
    for trans in transactions:
        if trans.Product == in_product:
            return trans
    return None
