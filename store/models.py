from random import choices
from secrets import choice
from django.db import models
from django.contrib.auth.models import User
import datetime

from django.forms import Textarea

# Create your models here.

		

    


class Category(models.Model):
	name = models.CharField(max_length=50)

	@staticmethod
	def get_all_categories():
		return Category.objects.all()

	def __str__(self):
		return self.name




# ------------products model-----------------------

S = [
    ('1' , 'Available'),
    ('2', 'Unavailable'),
    
]


class Products(models.Model):
    name = models.CharField(max_length=60)
    marked_price = models.IntegerField(default=0)
    selling_price = models.IntegerField(default=0)
    cost_price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    desc = models.TextField(max_length=500, default='Fresh and Nutritious with good packaging')
    image = models.ImageField(upload_to='store/images/',default="")
    status = models.CharField(max_length=100, choices=S, default='1')
    pub_date = models.DateField()


    


    def __str__(self):
        return self.name
  
    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter(id__in=ids)
  
    @staticmethod
    def get_all_products():
        return Products.objects.all()
  
    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter(category=category_id)
        else:
            return Products.get_all_products()



#------- customer model--------------

class Customer_profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    First_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    pincode = models.CharField(max_length=10)
    locality = models.CharField(max_length=50)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    landmark = models.CharField(max_length=100)
    
    def __str__(self):
        str1 = str(self.user) + str("_") + str(self.state)
        return str1

class ProductsSellerFarmer(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='store/images/',default="")
    daily_selling_quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=100, choices=S, default='1')
    seller_name = models.CharField(max_length=200)
    phone = models.ForeignKey(Customer_profile, on_delete=models.CASCADE)

    def __str__(self):
        str1 = str(self.product) + str("_") + str(self.phone.state) + str("_") + str(self.daily_selling_quantity) + str("_") + str(self.status)
        return str(str1)




class Order(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer_profile, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1)
    price = models.FloatField(default=0)
    notify_seller = models.ForeignKey(ProductsSellerFarmer, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(default=datetime.datetime.today)
    

    class Meta:
        ordering = ['-date']



    def __str__(self):
        return str(self.customer)

class Cart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer_profile, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    #price = models.IntegerField(default=0)
    date = models.DateField(default=datetime.datetime.today)
    


    def __str__(self):
        return str(self.customer)


class Contact(models.Model):
    reason = models.TextField()
    phone = models.CharField(max_length=50)
    time_slot = models.CharField(max_length=100)
    date = models.DateField(default=datetime.datetime.today)


    def __str__(self):
        return str(self.phone)

Status = [
    ('1' , 'Ordered'),
    ('2', 'On the way'),
    ('3', 'Delivered'),
    ('4', 'Refused'),
]


class ProductTracker(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=200, default="")
    productStatus = models.CharField(max_length=100, choices=Status, default='1')


    def __str__(self):
        str1 = str(self.order) + str("_") + str(self.product)
        return str(str1)




class ProductsSeller(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    seller_state = models.CharField(max_length=100)
    marked_price = models.IntegerField(default=0)
    selling_price = models.IntegerField(default=0)
    cost_price = models.IntegerField(default=0)

    class Meta:
        unique_together = [("product", "seller_state")]


    def __str__(self):
        str1 = str(self.product) + str("_") + str(self.seller_state)
        return str(str1)



