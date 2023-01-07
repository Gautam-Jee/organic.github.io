from dataclasses import fields
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from numpy import delete
from .models import Cart, Products, Customer_profile, Order, Contact, ProductTracker, ProductsSeller, ProductsSellerFarmer
from .forms import EditProfile, CaptchaTestForm, ProductSeller, EditProductSellerfarmer
import itertools


def index(request):
    # products= Products.objects.all()
    products = []
    catprods = Products.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        productscat = Products.objects.filter(category=cat).order_by('status')
        products.append(productscat)

    
        


    context = {'products': products}
    try:
        if request.user.is_authenticated:
            cartitems = Cart.objects.filter(
                customer=request.user.customer_profile.id)
            adminproducts = ProductsSeller.objects.filter(seller_state=request.user.customer_profile.state)
            ids = []
            for cartitem in cartitems:
                ids.append(cartitem.product.id)
            context = {'products': products, 'ids': ids, 'adminproducts':adminproducts}
            return render(request, "index.html", context)

    except:
        context = {'products': products}
        return render(request, "index.html", context)

    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        reason = request.POST['issue']
        phone = request.POST['phone']
        time = request.POST['time']
        contact = Contact(reason=reason, phone=phone, time_slot=time)
        contact.save()
        messages.success(request, "Contact details successfully sent Now Continue your shopping")
        return redirect("/contact")
    
    return render(request, "contact.html")


def tracker(request, id):
    order = Order.objects.get(pk=id)
    # producttrack = ProductTracker(order=order, product=order.product.name)
    # producttrack.save()
    track = ProductTracker.objects.get(order=id)
    return render(request, "tracker.html", {'order':order, 'track': track})

def searchMatch(query, item):
    if query.lower() in item.name.lower() or query.lower() in item.category.name.lower() or query.lower() in item.desc.lower():
        return True
    return False


def search(request):
    s=0
    query = request.GET['search']
    products = []
    catprods = Products.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        productscat = Products.objects.filter(category=cat).order_by('status')
        prod = [item for item in productscat if searchMatch(query, item)]
        if len(prod) == 0:
            s=s+1
        products.append(prod)

    info = "No Search Results found Please try another one"

    if s == 4:
        return render(request, "search.html", {'info':info})


    context = {'products': products}
    try:
        if request.user.is_authenticated:
            cartitems = Cart.objects.filter(customer=request.user.customer_profile.id)
            ids = []
            for cartitem in cartitems:
                ids.append(cartitem.product.id)
            context = {'products': products, 'ids': ids}
            return render(request, "search.html", context)

    except:
        context = {'products': products}
        return render(request, "search.html", context)

    #return render(request, "search.html", context)

        

    

def farmers(request):
    if request.user.is_anonymous:
        return redirect("/login")

    try:
        obj = Customer_profile.objects.get(pk=request.user.customer_profile.id)
        farmerproducts = ProductsSellerFarmer.objects.filter(phone=request.user.customer_profile.id)
        adminproducts = ProductsSeller.objects.filter(seller_state=request.user.customer_profile.state)
        
            
                
    except:
        messages.warning(request, "Warning! Please add address before go to seller page")
        return redirect("/profile")

    
    if request.method == "POST":
        obj = Customer_profile.objects.get(pk=request.user.customer_profile.id)
        form = ProductSeller(request.POST, request.FILES)
        prod = request.POST['product']
        for products in farmerproducts:
            a = products.product.id    
            if int(prod) == int(a) :
                messages.warning(request, f"Warning! {products.product} is already added please add another product")
                return redirect("/farmers")

       
        if form.is_valid():
            add_product=form.save(commit=False)
            add_product.phone = request.user.customer_profile
            add_product.seller_name = obj.First_name
            add_product.save()
            messages.success(request, "Product has been saved successfully now add another product")
            return redirect("/farmers")

    else:
        form = ProductSeller()


       
    
    
    return render(request, "farmers.html", {'form' : form, 'farmerproducts':farmerproducts, 'adminproducts':adminproducts})





def productview(request):
    return render(request, "productview.html")


def checkout(request, id):
    if request.user.is_anonymous:
        return redirect("/login")
    
    form = CaptchaTestForm()

    if request.method == "POST":
        obj = Customer_profile.objects.get(pk=request.user.customer_profile.id)
        obj1 = Products.objects.get(pk=id)
        quantity = request.POST['quantity']
        price = request.POST['totalprice']
        order = Order(product=obj1, customer=obj,
                      quantity=quantity, price=price)
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            order.save()
            producttrack = ProductTracker(order=order, product=order.product.name)
            producttrack.save()
            messages.success(request, "Order has been placed successfully Now continue your shopping")
            return redirect("/myorders")

        else:
            form = CaptchaTestForm()
            messages.warning(request, "Please fill captcha correctly")
    
    try:
        adminproducts = ProductsSeller.objects.filter(seller_state=request.user.customer_profile.state)

    except:
        messages.warning(request, "Warning! Please add address before go to cart")
        return redirect("/profile")

    
    products = Products.objects.get(pk=id)
    return render(request, "checkout.html", {'products': products, 'form': form, 'adminproducts':adminproducts})


def cart(request):
    if request.user.is_anonymous:
        return redirect("/login")

    form = CaptchaTestForm()
    try:
        cartitems = Cart.objects.filter(customer=request.user.customer_profile.id).order_by('-date')
        adminproducts = ProductsSeller.objects.filter(seller_state=request.user.customer_profile.state)
        ids = []
        cartid = []
        for cartitem in cartitems:
            ids.append(cartitem.product.id)
            cartid.append(cartitem.id)

        lengthofcart = len(ids)
        if request.method == "POST":
            obj = Customer_profile.objects.get(pk=request.user.customer_profile.id)
            i = 1
            for (id , cid) in zip(ids , cartid):
                a = str(i)
                obj1 = Products.objects.get(pk=id)
                obj2 = Cart.objects.get(pk=cid)
                quantity = request.POST['quantity_' + a]
                price = request.POST['price_' + a]
                order = Order(product=obj1, customer=obj, quantity=quantity, price=price)
                form = CaptchaTestForm(request.POST)
                if i == 1:
                    if form.is_valid():
                        order.save()
                        producttrack = ProductTracker(order=order, product=order.product.name)
                        producttrack.save()
                        i += 1
                        obj2.delete()


                    else:
                        form = CaptchaTestForm()
                        messages.warning(request, "Please fill captcha correctly")
                        return redirect("/cart")

                else:
                    order.save()
                    producttrack = ProductTracker(order=order, product=order.product.name)
                    producttrack.save()
                    i += 1
                    obj2.delete()


                    

            messages.success(request, "Order has been placed successfully Now continue your shopping")    
            return redirect("/myorders")
        return render(request, "cart.html", {'cartitems': cartitems, 'lengthofcart': lengthofcart, 'form': form, 'adminproducts':adminproducts})

    except:
        messages.warning(request, "Warning! Please add address before go to cart")
        return redirect("/profile")


def addcart(request, id):
    if request.user.is_anonymous:
        return redirect("/login")
    try:
        current = request.POST['current']
        obj = Customer_profile.objects.get(pk=request.user.customer_profile.id)
        obj1 = Products.objects.get(pk=id)
        cart = Cart(product=obj1, customer=obj)
        cart.save()
        return HttpResponseRedirect(current)
        #return redirect("/")
        
    
    except:
        messages.warning(request, "Warning! Please add address before add to cart")
        return redirect("/profile")


def profile(request):
    if request.user.is_anonymous:
        return redirect("/login")

    if request.user.is_authenticated:
        if request.method == "POST":
            user = User.objects.get(username=request.user.username)
            first_name = request.POST['fname']
            last_name = request.POST['lname']
            phone = request.POST['phone']
            email = request.user.email
            pincode = request.POST['pin']
            locality = request.POST['loc']
            address = request.POST['add']
            city = request.POST['city']
            state = request.POST['state']
            landmark = request.POST['mark']
            customer = Customer_profile(user=user, First_name=first_name, Last_name=last_name, phone=phone, email=email,
                                        pincode=pincode, locality=locality, address=address, city=city, state=state, landmark=landmark)
            customer.save()
            messages.success(request, "Address has been saved successfully")

        return render(request, "profile.html")


def registration(request):
    if request.method == "POST":
        phone = request.POST['phone']
        email = request.POST['e-mail']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        users = User.objects.all()

        for user in users:
            if user.username == phone:
                messages.warning(
                    request, "warning! this mobile number already exist try another one")
                return redirect('/registration')

        # check for the inputs valid
        if len(phone) < 10 or len(phone) > 10:
            messages.warning(
                request, "warning! Mobile number is not correct please fill the correct number")
            return redirect('/registration')

        if pass1 != pass2:
            messages.warning(
                request, "warning! Password not matched please fill correct password ")
            return redirect('/registration')

        user = User.objects.create_user(phone, email, pass1)
        user.first_name = fname
        user.last_name = lname
        user.save()
        messages.success(
            request, "you have registered successfully Login from here by  mobile number and password")
        return redirect('/login')

    else:
        return render(request, "registration.html")


def myorders(request):
    if request.user.is_anonymous:
        return redirect("/login")

    try:
        orders = Order.objects.filter(customer=request.user.customer_profile.id).order_by('-date')
        return render(request, "myorders.html", {'orders': orders})
    except:
        messages.warning(request, "Warning! Please add address before go to orders")
        return redirect("/profile")




def vegetables(request):
    products = Products.objects.filter(category='1').order_by('status')
    try:
        if request.user.is_authenticated:
            cartitems = Cart.objects.filter(
                customer=request.user.customer_profile.id)
            adminproducts = ProductsSeller.objects.filter(seller_state=request.user.customer_profile.state)
            ids = []
            for cartitem in cartitems:
                ids.append(cartitem.product.id)
            context = {'products': products, 'ids': ids, 'adminproducts':adminproducts}
            return render(request, "vegetables.html", context)

    except:
        context = {'products': products}
        return render(request, "vegetables.html", context)

    return render(request, "vegetables.html", {'products':products})


def fruits(request):
    products = Products.objects.filter(category='2').order_by('status')
    try:
        if request.user.is_authenticated:
            cartitems = Cart.objects.filter(
                customer=request.user.customer_profile.id)
            adminproducts = ProductsSeller.objects.filter(seller_state=request.user.customer_profile.state)
            ids = []
            for cartitem in cartitems:
                ids.append(cartitem.product.id)
            context = {'products': products, 'ids': ids, 'adminproducts':adminproducts}
            return render(request, "fruits.html", context)

    except:
        context = {'products': products}
        return render(request, "fruits.html", context)

    return render(request, "fruits.html", {'products':products})


def grains(request):
    products = Products.objects.filter(category='3').order_by('status')
    try:
        if request.user.is_authenticated:
            cartitems = Cart.objects.filter(
                customer=request.user.customer_profile.id)
            adminproducts = ProductsSeller.objects.filter(seller_state=request.user.customer_profile.state)
            ids = []
            for cartitem in cartitems:
                ids.append(cartitem.product.id)
            context = {'products': products, 'ids': ids, 'adminproducts':adminproducts}
            return render(request, "grains.html", context)

    except:
        context = {'products': products}
        return render(request, "grains.html", context)

    return render(request, "grains.html", {'products':products})



def flours(request):
    products = Products.objects.filter(category='4').order_by('status')
    try:
        if request.user.is_authenticated:
            cartitems = Cart.objects.filter(
                customer=request.user.customer_profile.id)
            adminproducts = ProductsSeller.objects.filter(seller_state=request.user.customer_profile.state)
            ids = []
            for cartitem in cartitems:
                ids.append(cartitem.product.id)
            context = {'products': products, 'ids': ids, 'adminproducts':adminproducts}
            return render(request, "flours.html", context)

    except:
        context = {'products': products}
        return render(request, "flours.html", context)

    return render(request, "flours.html", {'products':products})



def loginuser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(
                request, "you have logged in successfully Now add your address if already done continue your shopping")
            return redirect("/profile")

        else:
            messages.warning(
                request, "warning! please fill all the details correctly")
            return render(request, "login.html")
    return render(request, "login.html")


def logoutuser(request):
    logout(request)
    return redirect("/")


def edit_profile(request, id):
    if request.method == "POST":
        obj = Customer_profile.objects.get(pk=id)
        form = EditProfile(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Address has been updated successfully now continue your shopping")
            return redirect("/profile")

    else:
        obj = Customer_profile.objects.get(pk=id)
        form = EditProfile(instance=obj)

    return render(request, "edit_profile.html", {'form': form})

def edit_farmerproduct(request, id):
    if request.method == "POST":
        obj = ProductsSellerFarmer.objects.get(pk=id)
        form = EditProductSellerfarmer(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Product information has been updated successfully")
            return redirect("/farmers")

    else:
        obj = ProductsSellerFarmer.objects.get(pk=id)
        form = EditProductSellerfarmer(instance=obj)

    return render(request, "edit_farmerproduct.html", {'form': form})



def delete_item(request, id):
    obj = Cart.objects.get(pk=id)
    obj.delete()
    return redirect("/cart")

def delete_farmerproduct(request, id):
    obj = ProductsSellerFarmer.objects.get(pk=id)
    obj.delete()
    return redirect("/farmers")



def customer_orders(request):
    #try:
    adminproducts = ProductsSeller.objects.filter(seller_state=request.user.customer_profile.state)
    #orders = Order.notify_seller.filter(phone=request.user.customer_profile.id).order_by('-date')
    orders = Order.objects.all().order_by('-date')

    # except:
    #     messages.warning(request, "Warning! No Customers have ordered your items till now.")
    #     return redirect("/farmers")



    return render(request, "customer_orders.html", {'adminproducts': adminproducts, 'orders':orders})
