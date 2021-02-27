from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
from accounts.models import *
from datetime import datetime
from math import ceil
from sslcommerz_lib import SSLCOMMERZ
from pprint import pprint
from django.contrib.auth.models import User
import json
import ast
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
global cat_global
global purchaseDetails, totalPrice

sno = 0
purchaseDetails = {}
totalPrice = 0

# Create your views here.


def home(request):

    disProds = discountedProducts.objects.all().reverse()[0:3]
    products = Product.objects.all()
    latestProducts = products.order_by("-pub_date")
    advProds = DiscountAdvertisement.objects.all()
    subcats = SubCategories.objects.all()
    contacts = Contact.objects.all()
    print(products)
    n = len(products)
    nSlides = n//4 + ceil((n/4) + (n//4))
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = Categories.objects.all()
    catsHalfOne = cats[0:int(len(cats)/2)]
    catsHalfTwo = cats[int(len(cats)/2):]
    for cat in cats:
        prod = Product.objects.filter(category=cat.name)
        allProds.append([prod, range(1, nSlides), nSlides])
    cats2 = Categories.objects.all()
    params = {'allProds':allProds, 'products':products, 'contact':contacts, 'latestProducts':latestProducts,
              'n':0, 'cats':cats2, 'discProds':disProds, 'subcats':subcats, 'catsHalfOne':catsHalfOne, 'catsHalfTwo':catsHalfTwo, 'advProds':advProds}

    return render(request, 'index.html', params)
    # return HttpResponse(subcats_ll)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        message = request.POST.get('message')

        contactMsg = Contact(name=name, email=email,
                             contact=contact, message=message)
        contactMsg.save()
        messages.success(
            request, 'We have recieved your message successfully. We may contact you back if needed.')

    products = Product.objects.all()
    cats = Categories.objects.all()

    params = {'cats': cats}

    return redirect('/')


def addComment(request, category, ids):
    if request.user.is_authenticated:
        if request.method == 'POST':
            comment = request.POST['comment']
            add = Comments(userName=request.user.username, userID=request.user.id, productID=ids, dateTime=datetime.now(), comment=comment)
            add.save()
            return redirect('/products/'+str(category) + '/' + str(ids))
        else:
            return redirect('/products/'+str(category) + '/' + str(ids))
    else:
        return redirect('/products/'+str(category) + '/' + str(ids))



def indivProduct(request, category, ids):
    products = Product.objects.all()
    cats = Categories.objects.all()
    subcats = SubCategories.objects.all()
    comments = Comments.objects.filter(productID=ids)

    testProd = Product.objects.get(id=ids)
    # prods = testProd.values('product_name', 'sub_category',
    #                         'desc', 'price', 'presentPrice', 'image', 'id', 'slug', 'category')
    # prods = testProd.values()
    # subcats_l.append(testProd.sub_category)

    params = {'cats': cats, 'category': category, 'products': testProd, 'subcats':subcats, 'comments':comments, 'id':ids}
    return render(request, 'indivProducts.html', params)
    # return HttpResponse(testProd)


def indivProductDisc(request, category, ids):
    products = Product.objects.all()
    cats = Categories.objects.all()
    subcats = SubCategories.objects.all()

    testProd = discountedProducts.objects.get(id=ids)
    # prods = testProd.values('product_name', 'sub_category',
    #                         'desc', 'price', 'presentPrice', 'image', 'id', 'slug', 'category')
    # prods = testProd.values()
    # subcats_l.append(testProd.sub_category)

    params = {'cats': cats, 'category': category, 'products': testProd}
    return render(request, 'indivProduct.html', params)
    # return HttpResponse(testProd)




def allProducts(request, category):
    global cat_global
    cat_global = category
    products = Product.objects.all()
    cats = Categories.objects.all()
    subcats = SubCategories.objects.all()
    subcats_l = SubCategories.objects.filter(category=category)
    testProd = Product.objects.filter(category=category)
    prods = testProd.values('product_name', 'sub_category', 'category', 'presentPrice', 'desc', 'price', 'image',  'id', 'slug', 'discount')

    params = {'cats': cats, 'subcats': subcats, 'subcats_l': subcats_l,
              'category': category, 'products': prods}
    return render(request, 'allProducts.html', params)
    # return HttpResponse(subcats_l)


def subAllProducts(request, category, sub_category):
    products = Product.objects.all()
    cats = Categories.objects.all()
    testProd = Product.objects.filter(category=category)
    testProd2 = Product.objects.filter(
        category=category, sub_category=sub_category)
    prods2 = testProd2.values('product_name', 'sub_category', 'category', 'presentPrice', 'desc', 'price', 'image',  'id', 'slug', 'discount')
    subcats_l = SubCategories.objects.filter(category=category)
    subcats = SubCategories.objects.all()

    params = {'products': prods2, 'cats': cats,
              'category': category, 'subcats': subcats}
    return render(request, 'subProds.html', params)
    # return HttpResponse(prods)


def discountProducts(request):
    discProds = discountedProducts.objects.all()
    cats = Categories.objects.all()
    return render(request, 'discountedProducts.html', {'discProds':discProds, 'cats': cats})


def discountIndivProducts(request, productID):
    discounts = discountedProducts.objects.all()
    params = {'products': discountedProducts.objects.get(id=productID)}
    return render(request, 'indivProduct.html', params)


def about(request):
    products = Product.objects.all()
    cats_l = []
    for i in products:
        cats_l.append(i.category)
    cats_s = set(cats_l)
    cats = list(cats_s)

    params = {'cats': cats}

    return render(request, 'about.html', params)


def search(request):
    products = Product.objects.all()
    cats = Categories.objects.all()
    subcats = SubCategories.objects.all()

    if request.method == 'GET':
        src = request.GET.get('search')
        results = Product.objects.filter(product_name__icontains=src)
        resultFinal = results.values()

        print(results)
        if results.exists():
            params = {'cats': cats, 'products': resultFinal, 'subcats':subcats}
            return render(request, 'search-results.html', params)
        else:
            messages.success(request, 'No search results found :(')
            params = {'cats': cats, 'products': resultFinal, 'subcats':subcats}
            return redirect('/')


def checkout(request):
    subcats = SubCategories.objects.all()
    if request.user.is_authenticated:
        user = UserCustom.objects.get(username=request.user.username)
        contact = user.contact
        cats = Categories.objects.all()
        address = user.address
        params = {'contact':contact, 'address':address, 'cats':cats, 'subcats':subcats}
        return render(request, 'checkout.html', params)
    else: 
        messages.error(request, 'Please Log in first.')
        return redirect('/accounts/login')
    # return HttpResponse(str(tableList))


def payment(request):
    global purchaseDetails, totalPrice
    user = UserCustom.objects.get(username=request.user.username)
    if request.method == 'POST':
        totalPrice = request.POST.get('totalPrice')
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        purchaseDetails = request.POST.get('purchaseDetails')
        mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id='naser5f87eff1ddede', sslc_store_pass='naser5f87eff1ddede@ssl')
        mypayment.set_urls(
            success_url='http://127.0.0.1:8000/completeOrder/'+str(request.user.username), 
            fail_url='http://127.0.0.1:8000/incompleteOrder/'+str(request.user.username),
            cancel_url='http://127.0.0.1:8000/incompleteOrder/'+str(request.user.username), 
            ipn_url='http://127.0.0.1:8000/'
            ) 
        mypayment.set_product_integration(total_amount=Decimal(totalPrice), currency='BDT', product_category='Payment', product_name='Product', num_of_item=1, shipping_method='YES', product_profile='None')
        mypayment.set_customer_info(name=request.user.first_name, email=request.user.email, address1=address, address2=address, city='Dhaka', postcode='2231', country='Bangladesh', phone=contact)
        mypayment.set_shipping_info(shipping_to='Abir', address='Address', city='Dhaka', postcode='1209', country='Bangladesh')
        response_data = mypayment.init_payment()
        print(response_data)

        return redirect(response_data['GatewayPageURL'])
        
        
        # order = Purchases(discount=0, product_details=purchaseDetails, customerUsername=request.user.username, dates=datetime.now().strftime('%d-%m-%y'), totalPrice=totalPrice)
        # order.save()
        # cats = Categories.objects.all()
        # messages.success(request, 'Your Order has been taken successsfully')
        # params = {'cat':cats}
        # return render(request, 'checkoutComplete.html', params)


@csrf_exempt
def completeOrder(request, username1):
    global purchaseDetails, totalPrice
    cats = Categories.objects.all()
    order = Purchases(discount=0, product_details=purchaseDetails, customerUsername=username1, dates=datetime.now().strftime('%d-%m-%y'), totalPrice=totalPrice)
    order.save()
    purchases = str(purchaseDetails).replace('"', "'")
    for i, j in ast.literal_eval(purchases).items():
        print(i[2:])
        productIndiv = Product.objects.get(id=i[2:])
        productIndiv.sellingFrequency = int(productIndiv.sellingFrequency) + 1
        productIndiv.save()
    messages.success(request, 'Your Order has been taken successsfully')
    params = {'cat':cats}
    return render(request, 'checkoutComplete.html', params)

@csrf_exempt
def incompleteOrder(request, username1):
    return render(request, 'orderFail.html')



