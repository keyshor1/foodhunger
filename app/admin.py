from django.contrib import admin
from . models import Cart, Custom_Orders, Customer, OrderPlaced, Product, Review, Profile
from django.utils.html import format_html
from django.urls import reverse
# Register your models here.

@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'auth_token']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','selling_price', 'discounted_price', 'category', 'product_image']

@admin.register(Custom_Orders)
class Custom_OrdersModelAdmin(admin.ModelAdmin):
    list_display = ['custom_status', 'id', 'user', 'product', 'photo', 'date']
    

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'locality', 'city', 'state', 'zipcode']
    

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['status', 'id', 'user', 'customer', 'product', 'quantity', 'ordered_date']

@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ['status', 'id', 'user', 'product', 'rate', 'created_at', 'status']
    # readonly_fields = ['created_at',]