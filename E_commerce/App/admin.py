from django.contrib import admin
from .models import Product, Customer, Cart, payments

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','discount_price','category','product_image']


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','locality','city','state','zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(payments)
class PaymentsModelAdmin(admin.ModelAdmin):
    list_display = ['holdername','cardnumber','expiry_date','cvv']

# @admin.register(OrderPlaced)
# class OrderPlacedModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']


