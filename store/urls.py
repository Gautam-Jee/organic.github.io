from django.contrib import admin
from django.urls import path
from store import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.index, name='Home'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),
    path('about/', views.about, name='AboutUs'),
    path('contact/', views.contact, name='contact'),
    path('tracker <int:id>/', views.tracker, name='tracker'),
    path('search/', views.search, name='Search'),
    path('productview/', views.productview, name='ProductView'),
    path('checkout <int:id>/', views.checkout, name='checkout'),
    path('delete_item <int:id>/', views.delete_item, name='delete_item'),
    path('addcart <int:id>/', views.addcart, name='addcart'),
    path('cart/', views.cart, name='cart'),
    path('profile/', views.profile, name='profile'),
    path('registration/', views.registration, name='registration'),
    path('myorders/', views.myorders, name='myorders'),
    path('Vegetables/', views.vegetables, name='vegetables'),
    path('Fruits/', views.fruits, name='fruits'),
    path('Grains/', views.grains, name='grains'),
    path('Flours/', views.flours, name='flours'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('registration/', views.registration, name='registration'),
    path('edit_profile <int:id>/', views.edit_profile, name='edit_profile'),
    path('edit_farmerproduct <int:id>/', views.edit_farmerproduct, name='edit_farmerproduct'),
    path('delete_farmerproduct <int:id>/', views.delete_farmerproduct, name='delete_farmerproduct'),
    path('farmers/', views.farmers, name='farmers'),
    path('customer_orders/', views.customer_orders, name='customer_orders'),
    # path('captchafield <int:id>/', views.captchafield, name='captchafield'),

]
