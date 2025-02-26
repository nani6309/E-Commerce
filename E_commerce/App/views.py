from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from urllib import request
from .models import Product,Customer, Cart, payments
from django.db.models import Count
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Q
# import razorpay
# from django.conf import settings
# from paypal.standard.forms import PayPalPaymentsForm
# import uuid
# from django.urls import reverse


# Create your views here.
def home(request):
    return render(request,"app/home.html")

def AboutUs(request):
    return render(request,"app/aboutus.html")

def ContactUs(request):
    return render(request,"app/contactus.html")

class CategoryView(View):
    def get(self, request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render (request,"app/category.html",locals())
    
class CategoryTitle(View):
    def get(self,request,val):
        product=Product.objects.filter(title=val)
        title= Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html", locals())

class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,"app/productdetail.html",locals())
    

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render (request,"app/customerregistraion.html",locals())
    def post(self,request):
            form=CustomerRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Congratulations! User Registered Successfully")
            else:
                messages.warning(request,"Invalid Input Data")
            return render (request,"app/customerregistraion.html",locals())
    

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/profile.html', locals())
    

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())

class updateAddress(View):
    def get(self,request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name =  form.cleaned_data['name']
            add.locality =  form.cleaned_data['locality']
            add.city =  form.cleaned_data['city']
            add.mobile =  form.cleaned_data['mobile']
            add.state =  form.cleaned_data['state']
            add.zipcode =  form.cleaned_data['zipcode']
            add.save()
            messages.success(request,'Profile update successfully')
        else:
            messages.warning(request,'Invalid Input Data')
        return redirect('address')
    
def signout(request):
    logout(request)
    return redirect('login')
    
def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity*p.product.selling_price
        amount = amount + value
    totalamount = amount + 40
    return render(request, 'app/addtocart.html', locals())


class Checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value = p.quantity*p.product.selling_price
            famount= famount+value
        totalamount = famount+40
        return render(request,'app/checkout.html',locals())
    




def payment(request):
    if request.method == 'POST':
        holdername=request.POST.get('holdername')
        cardnumber = request.POST.get('cardnumber')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        payments.objects.create(
            holdername=holdername,
            cardnumber=cardnumber,
            expiry_date=expiry_date,
            cvv=cvv
        )
        return redirect('orderplaced')

    return render(request, 'app/paymentform.html')

def orderplaced(request):
    return render(request, 'app/orderplaced.html')

                  





def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))  #Q is for Mutiple filter conditions
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity*p.product.selling_price
            amount = amount + value
        totalamount = amount + 40
        #print(prod_id)
        data = {   
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount 
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))  #Q is for Mutiple filter conditions
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity*p.product.selling_price
            amount = amount + value
        totalamount = amount + 40
        #print(prod_id)
        data = {   
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount 
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))  #Q is for Mutiple filter conditions
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity*p.product.selling_price
            amount = amount + value
        totalamount = amount + 40
        #print(prod_id)
        data = {   
            'amount':amount,
            'totalamount':totalamount 
        }
        return JsonResponse(data)
    
    
