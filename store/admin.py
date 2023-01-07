from django.contrib import admin

# Register your models here.

from .models import Products, Category,Customer_profile, Order, Cart, Contact, ProductTracker, ProductsSeller, ProductsSellerFarmer

admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Customer_profile)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Contact)
admin.site.register(ProductTracker)
admin.site.register(ProductsSeller)
admin.site.register(ProductsSellerFarmer)