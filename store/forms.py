from dataclasses import fields
from pickle import READONLY_BUFFER
from tkinter import Widget
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import Customer_profile, Order, ProductsSellerFarmer
from captcha.fields import CaptchaField

class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()


class EditProfile(ModelForm):
    class Meta:
        model = Customer_profile
        fields = ('phone','pincode', 'locality', 'address', 'city', 'state', 'landmark')
    
class EditProductSellerfarmer(ModelForm):
    #seller_name = forms.CharField(disabled=True)
    class Meta:
        model = ProductsSellerFarmer
        fields = ( 'daily_selling_quantity', 'status',)




class ProductSeller(ModelForm):
    #seller_name = forms.CharField(disabled=True)
    class Meta:
        model = ProductsSellerFarmer
        fields = ('product', 'category', 'image', 'daily_selling_quantity', 'status',)
        
