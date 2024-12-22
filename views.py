from urllib import request
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Cart, Customer, OrderPlaced, Payment, Product, Wishlist
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
import paypalrestsdk 
# Create your views here.

@login_required
def home(request):
    totalitem =0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app1/home.html",locals())
@login_required
def about(request):
    totalitem =0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app1/about.html",locals())
@login_required
def contact(request):
    totalitem =0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app1/contact.html",locals())

@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self, request,val):
        totalitem =0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app1/category.html",locals())
@method_decorator(login_required, name='dispatch')
class CategoryTitle (View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem =0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render (request, "app1/category.html", locals())

@method_decorator(login_required, name='dispatch')
class ProductDetail(View):
    def get(self, request,pk):
        product = Product.objects.get(pk=pk)
        wishlist= Wishlist.objects.filter(Q(product=product) & Q(user=request.user))

        totalitem =0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, "app1/productdetail.html",locals())

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem =0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, "app1/customerregistration.html",locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, "app1/customerregistration.html",locals())
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form =CustomerProfileForm()
        totalitem =0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app1/profile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user= request.user
            name= form.cleaned_data['name']
            locality =form.cleaned_data['locality']
            city= form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode= form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! User Profile Saved Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app1/profile.html', locals())
@login_required
def address (request):
    add = Customer.objects.filter(user=request.user)
    totalitem =0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app1/address.html', locals())
@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    def get(self, request,pk):
        add = Customer.objects.get(pk=pk)
        form= CustomerProfileForm(instance=add)
        totalitem =0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app1/updateAddress.html', locals())
    def post(self, request,pk):
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! User Profile Updated Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")
@login_required   
def add_to_cart(request):
    # Get and clean the product ID
    prod_id = request.GET.get('prod_id', '').strip()
    if prod_id.endswith('/'):
        prod_id = prod_id[:-1]
    
    try:
        prod_id = int(prod_id)  # Convert to integer
    except ValueError:
        return HttpResponse("Invalid Product ID", status=400)
    
    # Fetch the product
    try:
        product = Product.objects.get(id=prod_id)
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)
    
    # Add to cart logic
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user, product=product)
    cart.quantity += 1
    cart.save()
    
    # Redirect to cart
    return redirect('showcart')
@login_required
def show_cart(request):
    user=request.user
    cart = Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity*p.product.discounted_price
        amount= amount + value
    totalamount=amount+40
    totalitem =0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app1/addtocart.html', locals())

@login_required
def show_wishlist (request):
    user = request.user
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem =len (Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render (request, "app1/wishlist.html", locals())

@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))

        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)

        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount += value

        totalamount = famount + 40
        context = {
            "add": add,
            "cart_items": cart_items,
            "totalamount": totalamount,
            "totalitem": totalitem,
            "wishitem": wishitem,
        }
        return render(request, "app1/checkout.html", context)

    def post(self, request):
        cust_id = request.POST.get("custid")
        totalamount = request.POST.get("totamount")

        # Validate selected customer address
        try:
            customer = Customer.objects.get(id=cust_id)
        except Customer.DoesNotExist:
            messages.error(request, "Invalid shipping address.")
            return redirect("/checkout/")

        # Configure PayPal
        paypalrestsdk.configure(
            {
                "mode": "sandbox",  # Use "live" for production
                "client_id": settings.PAYPAL_CLIENT_ID,
                "client_secret": settings.PAYPAL_SECRET,
            }
        )

        # Create PayPal Payment
        payment = paypalrestsdk.Payment(
            {
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": request.build_absolute_uri(f"/paymentdone/?cust_id={cust_id}"),
                    "cancel_url": request.build_absolute_uri("/checkout/"),
                },
                "transactions": [
                    {
                        "item_list": {
                            "items": [
                                {
                                    "name": "Order",
                                    "sku": "001",
                                    "price": str(totalamount),
                                    "currency": "EUR ",
                                    "quantity": 1,
                                }
                            ]
                        },
                        "amount": {"total": str(totalamount), "currency": "EUR"},
                        "description": "This is the payment description.",
                    }
                ],
            }
        )

        if payment.create():
            payment_id = payment.id
            Payment.objects.create(
                user=request.user,
                amount=totalamount,
                paypal_payment_id=payment_id,
            )
            for link in payment.links:
                if link.rel == "approval_url":
                    return redirect(link.href)  # Redirect to PayPal for approval
        else:
            print(payment.error)  # Log error for debugging
            messages.error(request, "Error creating PayPal payment. Please try again.")
            return redirect("/checkout/")
@login_required
def payment_done(request):
    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")
    cust_id = request.GET.get("cust_id")

    # Validate selected customer
    try:
        customer = Customer.objects.get(id=cust_id)
    except Customer.DoesNotExist:
        messages.error(request, "Invalid customer ID.")
        return redirect("/checkout/")

    # Execute PayPal payment
    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        # Payment succeeded
        payment_record = Payment.objects.get(paypal_payment_id=payment_id)
        payment_record.paid = True
        payment_record.save()

        # Place orders
        cart = Cart.objects.filter(user=request.user)
        for c in cart:
            OrderPlaced.objects.create(
                user=request.user,
                customer=customer,
                product=c.product,
                quantity=c.quantity,
                payment=payment_record,
            )
            c.delete()

        messages.success(request, "Payment successful! Order placed.")
        return redirect("orders")
    else:
        print(payment.error)  # Log error for debugging
        messages.error(request, "Payment failed. Please try again.")
        return redirect("/checkout/") 

    # #To save order details
    # cart=Cart.objects.filter(user=user)
    # for c in cart:
    #     OrderPlaced(user=user, customer =customer, product=c.product, quantity=c.quantity, payment= payment).save()
    #     c.delete()
    # return redirect("orders")   
@login_required
def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))

    order_placed = OrderPlaced.objects.filter(user=request.user)
    if not order_placed.exists():
        messages.info(request, "You have no orders yet.")
    return render(request, 'app1/orders.html', locals())


def plus_cart(request):
    if request.method=="GET":
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.quantity+=1
        c.save()
        user= request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount= amount + value
        totalamount=amount+40
        #print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method=="GET":
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.quantity-=1
        c.save()
        user= request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount= amount + value
        totalamount=amount+40
        #print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method=="GET":
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.delete()
        user= request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount= amount + value
        totalamount=amount+40
        #print(prod_id)
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def plus_wishlist (request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist (user=user, product=product).save()
        data={
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse (data)

def minus_wishlist (request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
            'message': 'Wishlist Remove Successfully',
        }
        return JsonResponse (data)
@login_required    
def search(request):
    # Safely get the 'search' parameter with a default value of an empty string
    query = request.GET.get('search', '').strip()
    
    totalitem = 0
    wishitem = 0
    
    if request.user.is_authenticated:
        # Count the items in the user's cart and wishlist
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = Wishlist.objects.filter(user=request.user).count()
    
    # Only filter products if a query is provided
    product = Product.objects.filter(Q(title__icontains=query)) if query else []
    
    # Render the template with the context
    return render(request, "app1/search.html", {
        'query': query,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'product': product,
    })

import paypalrestsdk

# Set up PayPal environment
paypalrestsdk.configure({
    "mode": "sandbox",  # Can also be 'live' for production
    "client_id": "AZ0FqSbDnHa9zHfT1htCKiH-P9aU198A3v5c2LhE8c4pBmuvio-gkJkYr3adLIwPUZqr7A_7Yy975cxX",
    "client_secret": "EGBOkY1bdfjmqcw5ZmENq8R_LA5szVb7FzzsWZWNvPduaXsvn0NbLC5fL3d16nrxQ9tXUVuVHwU0a7J8"
})

# Test the configuration
if paypalrestsdk.api == "sandbox":
    print("PayPal SDK configured successfully in Sandbox mode.")
else:
    print("PayPal SDK not configured correctly.")

