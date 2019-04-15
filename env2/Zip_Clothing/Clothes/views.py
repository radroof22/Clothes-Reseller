from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import string, random
## Accounts
'''
Accounts
*poop-ewwewweww
*Tyrone-passpass
'''
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from Zip_Clothing.settings import TAKE_HOME

# Create your views here.
import stripe
from Zip_Clothing.settings import stripe_publishable_key, stripe_secret_key

stripe.api_key = stripe_secret_key

## Home
def Home(request):
    # Create 2x3 List of random products to display on home page
    randomized_products = [[random.choice(models.Product.objects.all()) for _ in range(2)] for _ in range(3)]
    return render(request, "Clothes/home.html", {"user": request.user, "random_products":randomized_products})


@login_required
def Profile(request):
    ## Seller Oriented Displays
    # Get User Posted Products
    user_posted_products = models.Product.objects.filter(Seller=request.user)
    # Get transaction for notifications
    user_transactions = list(filter(None, [models.get_Transaction_by_Product_or_None(posted_prod) for posted_prod in user_posted_products]))
    
    ## Buyer Oriented Displays
    # Get transactions that buyer is involved in
    buy_trans = models.Transaction.objects.filter(Buyer=request.user)
    return render(request, "Account/prof_update.html", {"user_posted_products":user_posted_products, 
                                                        "user_transactions": user_transactions, 
                                                        "buy_transactions":buy_trans})
def Login(request):
    rand__clothes = [random.choice(models.Product.objects.all()) for _ in range(5)]
    error = False
    if request.method == "POST":
        username = request.POST["Username"]
        password = request.POST["Password"]
        # see if user exists
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # If user credential corr.
            login(request, user)
            if request.get_full_path() == "/accounts/login/":
                # Redirect to profile page
                return redirect("Profile")
            # else:
                
        else:
            error = True
    return render(request, "Account/login.html", {"ex_clothes": rand__clothes, "error":error})
@login_required
def Logout(request):
    logout(request)
    return redirect("Home")
def Sign_Up(request):
    rand__clothes = [random.choice(models.Product.objects.all()) for _ in range(5)]
    if request.method == "POST":
        # Get Form Fields
        username = request.POST["Username"]
        password = request.POST["Password"]
        email = request.POST["Email"]
        # create user
        user = User.objects.create_user(username, email, password)
        user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # If user credential corr.
            login(request, user)
            # Redirect to profile page
            return redirect("Profile")
    return render(request, "Account/register.html", {"ex_clothes": rand__clothes})


## Products
from . import models
from django.core.files.storage import FileSystemStorage
import random
def Create_Product(request):
    if request.method == "POST" and request.FILES['Image']:
        # Get simple forms
        name = request.POST["Name"]
        price = request.POST["Price"]
        description = request.POST["Description"]
        size = request.POST["Size"]

        # Get Image
        image_up = request.FILES["Image"]
        fs = FileSystemStorage()
        filename = fs.save("Image- {}:{}".format(name, request.user.username), image_up)

        # Create new instance of Product
        model_filled = models.Product.objects.create(Name=name, Description=description, Size=size, Price=price, Seller=request.user, Image=filename)
        model_filled.save()
        return redirect("Product_Detail")
    return render(request, "Product/create_product.html", {"user":request.user, })
def Product_List(request):
    # Gets random 20 products to show to the user
    randomized_products = [random.choice(models.Product.objects.all()) for _ in range(20)]
    returned_products = []
    for i in range(0, len(randomized_products), 4):
        returned_products.append(randomized_products[i:i + 4])
    return render(request, "Product/list.html", {"view_products": returned_products})
@login_required
@csrf_exempt
def Detail_Product(request, prod_id):
    # Gets proper product via id in url
    product_fetched = get_object_or_404(models.Product, pk=prod_id)

    if request.method == "POST":
        # Check if seller is viewing
        if request.user == product_fetched.Seller:
            # Seller wants to delete
            # Delete function is here
            product_fetched.delete()
            # Redirect to profile
            return redirect("Profile")
    return render(request, "Product/detail.html", {
            "user":request.user, 
            "product": product_fetched, 
            "is_owner": request.user == product_fetched.Seller, 
            "pub_key": stripe_publishable_key,
            "prod_price": int(product_fetched.Price) * 100
            })

def Charge(request):
    # 4242 4242 4242 4242
    product = models.Product.objects.get(id=int(request.POST["Prod_id"]))
    if request.method == "POST":
        
        amount = product.Price * 100
        customer = stripe.Customer.create(email=request.user.email,
                                            source=request.POST["stripeToken"])
        charge = stripe.Charge.create(
            customer=customer.id,
            amount = int(amount),
            currency = "usd",
            description = "Zip Trading is Charging for the purchase of '{}' for ${}".format(product.Name, product.Price)
        )
        ch = stripe.Charge.retrieve(charge.id)
       
        product.Bought = True
    return render(request, "Payment/charge.html", {"product": product})

def Shipping_Address(request):
    if request.method == "POST":
        Shipping_Location=request.POST["address"]
        product = models.Product.objects.get(id=int(request.POST["Prod_id"]))
        models.Transaction.objects.create(Shipping_Address=Shipping_Location, Buyer=request.user, Product=product)
    return redirect("Clothes:Profile")
def Confirm_Shipping(request, trans_id):
    transaction = models.Transaction.objects.get(id=trans_id)
    if request.user != transaction.Product.Seller:
        return redirect("Profile")
    if request.method == "POST":
        shipping_proof = request.POST["image_shipping"]
        transaction.Shipping_Receipt = shipping_proof
        transaction.Shipped = True
        transaction.save()
        return redirect("Profile")
    return render(request, "Post_Transaction/conf-shipping.html", {})
def Confirm_Receive(request, trans_id):
    transaction = models.Transaction.objects.get(id=trans_id)
    if request.user != transaction.Buyer:
        return redirect("Profile'") # Error Misc
    
    if request.method == "POST":
        transaction = models.Transaction.objects.get(id=trans_id)
        
        transaction.Complete = True
        transaction.save()

        
        return redirect("Profile")
    return render(request, "Post_Transaction/confirm_recieve.html", {"trans": transaction})
def Off_Notifications(request, trans_id):
    transaction = models.Transaction.objects.get(id=trans_id)
    buyer = transaction.Buyer
    seller = transaction.Product.Seller
    if request.user == buyer:
        transaction.Viewing_Buyer = False
        transaction.save()
    elif request.user == seller:
        transaction.Viewing_Seller = False
        transaction.save()
    return redirect("Profile")
def Claim_Cash(request, trans_id):
    transaction = models.Transaction.objects.get(id=trans_id)
    product = transaction.Product
    if request.user == product.Seller:
        if request.method == "POST":
            # Make sure the user that is requesting cash is actually the seller
            account = stripe.Account.retrieve(request.POST["stripeAccount"])
            stripe.Payout.create(
                amount = int(round(float(product.Price) *(1-TAKE_HOME), 2) * 100),
                currency="usd",
                destination = account,
            )
        else:
            return render(request, "Post_Transaction/claim_cash.html", {})
    else:
        return redirect("Profile")
