from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import AnonymousUser

# Python Imports
import random

# Personal Model Imports
from . import models
from . import forms

# Django-Payments
from payments import get_payment_model, RedirectNeeded

# Paypal
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
Handle_Cart = models.Cart_Handler()

class Paypal_Handle:
    def __init__(self, business_account, notify_url, return_url, cancel_return):
        self.business_account = business_account
        self.notify_url = notify_url
        self.return_url = return_url
        self.cancel_return = cancel_return

    def gen_tranaction_form_dict(self, request, cost_id, cost_indiv_item, item_name):
        return {
                "business": self.business_account,
                "amount": cost_indiv_item,
                "item_name": item_name,
                "invoice": cost_id,
                "notify_url": request.build_absolute_uri(reverse(self.notify_url)),
                "return_url": request.build_absolute_uri(reverse(self.return_url)),
                "cancel_return": request.build_absolute_uri(reverse(self.cancel_return)),
            }

paypal_handler = Paypal_Handle("rupangm@hotmail.com", "paypal-ipn", "Profile", "List")


def Home(request):
    return render(request, "Clothes/home.html", {})

def ListofProducts(request):
    # If person has searched for a given item in the shop
    if request.method == "POST":
        search_keyword = request.POST["search_for"]
        search_results = models.Clothing_Post.objects.filter(Name__contains=search_keyword)
        return render(request, "Clothes/ClothingList.html", {"Clothing": search_results, "searched": search_keyword})
    # If person is just casually searching for clothes, generate 30 random clothes posting that are up
    # WARNING: 3 is experimental number
    entrys_to_return = 3 
    random_30_posts_posts = random.sample(list(models.Clothing_Post.objects.all()), entrys_to_return)
    return render(request, "Clothes/ClothingList.html", {"Clothing": random_30_posts_posts, "searched":False})

@login_required
def RequirePaypal(request):
    if request.user == AnonymousUser:
        return HttpResponseRedirect(reverse("Login"))
    if request.method == "POST":
        print(request.POST)
        paypal_account = request.POST.get("paypal")
        # Add to cart
        # Make cart if user doesn't have one
        Handle_Cart.edit_paypal_cart(request.user, paypal_account)
        return HttpResponseRedirect(reverse("Profile")) 
    return render(request, "Clothes/Paypal_Required.html", {})

def ProductDetail(request, id):
    clothing = models.Clothing_Post.objects.get(id=id)
    if request.method == "POST":
        if type(request.user) == AnonymousUser:
            # if use is not signed in
            return HttpResponseRedirect(reverse("Login"))
        if request.user == clothing.User:
            #if user wants to delete post
            clothing.delete()
        elif Handle_Cart._get_cart_by_user(request.user) and Handle_Cart._get_cart_by_user(request.user).Paypal_Account != None:
            # Create a payment init for buying
            payment_creater = models.Payment(Item=clothing).save()
            # Redirect to purchasing page
            return HttpResponseRedirect(reverse("Purchase_Confirmation", kwargs={"id": clothing.id}))
        else:
            # Need paypal account
            print(Handle_Cart._get_cart_by_user(request.user))
            return HttpResponseRedirect(reverse("Paypal_require"))
        
        return HttpResponseRedirect(reverse("Profile"))

    return render(request, "Clothes/ClothingDetail.html", {"clothing": clothing})

@login_required
def Profile(request):
    if request.method == "POST":
        try:
            # CLEAR CART
            item_to_del = request.POST["item_t_delete"]
            if item_to_del == "ALL":
                Handle_Cart.reset_cart(request.user)
            else:
                Handle_Cart.remove_item_from_cart(request.user, item_to_del)
            #return HttpResponseRedirect(reverse("Profile"))
        except Exception:
            try:
                # Buy items
                buy_items = request.POST["buy_times"]
                if buy_items == "ALL":
                    return HttpResponseRedirect(reverse("Purchase_Confirmation"))
            except Exception:
                # Check for Shipping 
                meta_data = request.POST["meta_ship"]
                post_id, action = meta_data.split(",")
                if action == " confirm":
                    purchase_object = models.Clothing_Purchase.objects.get(id=post_id)
                    purchase_object.Delivered = True
                    purchase_object.save()
                elif action == " cancel":
                    # IF USER WANTS TO CANCEL ADD STUFF
                    pass
    user = request.user
    current_posts = models.Clothing_Post.objects.filter(User=user)
    current_active_posts = []
    current_purchased_posts = []
    for post in current_posts:
        try:
            purchase_waiting = models.Clothing_Purchase.objects.get(Clothing_post=post)
            current_purchased_posts.append(purchase_waiting)
            print("AS")
        except models.Clothing_Purchase.DoesNotExist:
            current_active_posts.append(post)
    # Shoudl redirect to cart registration?
    if not Handle_Cart.get_cart(request.user, if_has=True):
        # If they don't have a cart
        return HttpResponseRedirect(reverse("Paypal_require"))
    print(current_purchased_posts)
    return render(request, "Clothes/Profile.html", {"current_purchased_posts":current_purchased_posts, "current_active_posts":current_active_posts, "cart": Handle_Cart.get_cart(request.user)})

class NewClothing(CreateView):
    model = models.Clothing_Post
    fields = ["Name", "Description", "Image", "Price"]
    exclude = ["User", "DateTime_Posted"]
    template_name = "Clothes/NewClothing.html"

    def get(self, request):
        # Make sure person is logged in
        if request.user == AnonymousUser:
            return HttpResponseRedirect(reverse("Login"))
        if not Handle_Cart._get_cart_by_user(request.user):
            print(Handle_Cart._get_cart_by_user(request.user))
            # user doesn't have a cart
            # Make them create a cart so we can log their paypal account
            return HttpResponseRedirect(reverse("Paypal_require"))
        return super().get(request)

    def form_valid(self, form):
        
        clothing_post = form.save(commit=False)
        clothing_post.User = self.request.user
        
        clothing_post.save()
        id_ = clothing_post.id
        return HttpResponseRedirect(reverse("ClothingDetail", kwargs={"id":id_}))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('Paypal_require')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def Confirm_Purchase(request, id):
    # Get cart item
    item = get_object_or_404(models.Clothing_Post, id=id)

    if request.method == "POST":
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        address = request.POST.get("address")

        # User wants to buy
        Payment = get_payment_model()
        payment = Payment.object.create(
            variant = "default",
            description = "Purchase of Clothing",
            total = Item.Price,
            billing_first_name = firstName,
            billing_last_name = lastName,
            billing_address_1 = address
        )
    
    payment = get_object_or_404(get_payment_model(), Item=item)
    # try:
    #     form = payment.get_form(data=request.POST or None)
    # except RedirectNeeded as redirect_to:
    #     return redirect(str(redirect_to))
    form = payment
    return render(request, "Clothes/Purchase_Confirm.html", {"item":item, 'form':form})

@login_required
def Last_Payment_Stop(request):
    #curr_item = if not list(Handle_Cart.get_cart(request.user))[0]
    pass
    @login_required

@login_required
def Payment_Failure(request):
    return render(request, "Clothes/failed_transaction.html", {})

@login_required
def Payment_Success(request):
    return render(request, "Clothes/success_transaction", {})

@login_required
def Shipping_Confirm(request, id):
    transaction = models.Clothing_Purchase.objects.get(id=id)
    return render(request, "Clothes/Shipping_Confirm.html", {})