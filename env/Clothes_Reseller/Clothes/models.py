from django.db import models
from django.contrib.auth import get_user_model, get_user
from django.conf import settings
from django.db.models.query import EmptyQuerySet
from django.shortcuts import get_object_or_404
# Create your models here.

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Clothing_Post(models.Model):
    Name = models.CharField(max_length=140)
    Description = models.TextField()
    User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
    )
    DateTime_Posted = models.DateTimeField(auto_now_add=True)
    Image = models.ImageField()
    Price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return "{}-{}".format(self.User, self.Name)

class Clothing_Purchase(models.Model):
    Clothing_post = models.ForeignKey(Clothing_Post)
    Buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
    )
    Address = models.CharField(max_length=140)
    DateTime_Purchased = models.DateTimeField(auto_now_add=False)
    Delivered = models.BooleanField()

    def __str__(self):
        return "{}: {} = {}".format(self.Clothing_post, self.Buyer, self.Delivered)

# For django-payment
from decimal import Decimal

from payments import PurchasedItem
from payments.models import BasePayment

class Payment(BasePayment):
    Item = models.ForeignKey(Clothing_Post)
    def get_failure_url(self):
        return  HttpResponseRedirect(reverse("Trans_Fail"))

    def get_success_url(self):
        return HttpResponseRedirect(reverse("Trans_Success"))

    def get_purchased_items(self, id):
        # Get proper product
        item = get_object_or_404(Clothing_Post, id=id)
        # yield PurchasedItem(name=item.Name, sku=item.Name[:4],
        #                     quantity=1, price=item.Price, currency='USD')
        yield PurchasedItem(name='The Hound of the Baskervilles', sku='BSKV',
                            quantity=9, price=Decimal(10), currency='USD')

class User_Cart(models.Model):
    User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
    )
    Paypal_Account = models.CharField(max_length=16)

    class Meta:
        unique_together = (('User', 'Paypal_Account'),)

    def __str__(self):
        return self.User.username
    
class Cart_Item(models.Model):
    Clothing_Item = models.ForeignKey(Clothing_Post)
    Cart = models.ForeignKey(User_Cart)

    def __str__(self):
        return "{}:{}".format(self.Clothing_Item.Name, self.Cart.User.username)

class Cart_Handler:
    def add_item(self, user, item_id):
        """ Add item to cart: (User, Clothing_Post: Id) => None """
        cart = self._get_cart_by_user(user)
        _, _ = Cart_Item.objects.get_or_create(
            Clothing_Item=Clothing_Post.objects.get(id=item_id),
            Cart=cart
            )

    def create_cart(self, user, paypal):
        """ Create Cart for User if Doesn't Have One: (User) => (Cart/None['User already has a cart']"""
        _, _ = User_Cart.objects.get_or_create(User=user, Paypal_Account=paypal)
    
    def edit_paypal_cart(self, user, paypal):
        cart, _ = User_Cart.objects.get_or_create(User=user)
        cart.Paypal_Account = paypal
        cart.save()

    def _get_cart_by_user(self, user):
        """ Get User_Cart for User: (User) => (Cart) """
        cart =  User_Cart.objects.get(User=user)
        return cart

    def if_has(self, user):
        try:
            _ = self._get_cart_by_user(user)
            return True
        except Exception:
            return False

    def get_cart(self, user, if_has=False):
        """ Get Cart via User: (User) => (Items[]) """
        if not if_has:
            cart = self._get_cart_by_user(user)
            items = Cart_Item.objects.filter(Cart=cart)
            if len(items) == 0:
                return None
            else:
                return items
        else:
            return self.if_has(user)
        
    def reset_cart(self, user):
        """ Clear cart of all items: (User) => () """
        cart = self._get_cart_by_user(user)
        Cart_Item.objects.filter(Cart=cart).delete()

    def remove_item_from_cart(self, user, cart_item_id):
        cart = self._get_cart_by_user(user)
        Cart_Item.objects.get(id=cart_item_id).delete()

