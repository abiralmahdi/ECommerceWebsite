from django.shortcuts import render, HttpResponse, redirect
from home.models import *
from home.views import*
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate

# Create your views here.
def login(request):
    products= Product.objects.all()
    cats_l = []
    for i in products:
        cats_l.append(i.category)
    cats_s = set(cats_l)
    cats = list(cats_s)
    params={'cats':cats}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Successfully logged in, ' + str(user.first_name) + ' ' + str(user.last_name) + '!')
            return redirect('/')
        else:
            messages.error(request, 'Incorrect credentials')
            return redirect('/accounts/login')
            
    else:
        return render(request, 'login.html', params)


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    products= Product.objects.all()
    cats_l = []
    for i in products:
        cats_l.append(i.category)
    cats_s = set(cats_l)
    cats = list(cats_s)

    if request.method == 'POST':
        uname = request.POST.get('uname')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        password = request.POST.get('password')
        c_password = request.POST.get('c-password')

        if password == c_password:
            user = User.objects.create_user(uname, email, password)
            user.first_name = fname
            user.last_name = lname
            user.save()

            user2 = UserCustom(fname = fname, lname=lname, username=uname, email=email, contact=contact, address=address, 
                                password=password, no_of_orders=0,)
            user2.save()

            messages.success(request, 'You have created your account successfully!')
            user = auth.authenticate(username=uname, password=password)
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Your passwords does not match.')
    params={'cats':cats}
    return render(request, 'user-register.html', params)



def userDashboard(request, uname):
    if request.user.is_authenticated and request.user.username == uname:
        products = Product.objects.all()
        purchases = Purchases.objects.filter(customerUsername=uname)
        
        # hist_list_final = []
        # i_list = []
        # hist_list = []
        # h = []
        # cats_l = []
        # for i in products:
        #     cats_l.append(i.category)
        # cats_s = set(cats_l)
        # cats = list(cats_s)

        # user2 = UserCustom.objects.get(username=uname)
        # ords = int(user2.no_of_orders)
        # hist = ast.literal_eval(user2.order_history)
        # try:
        #     for key, value in hist.items():
        #         h.append(list(value.values()))
        #         for key1, value1 in value.items():
        #             if key1 == 'total_price':
        #                 break
        #             else:
        #                 hist_list.append(value1)
        #     params={'cats':cats, 'no_of_orders': ords, 'history_set': h}
        #     return render(request, 'user-dashboard.html', params)
        # except:
        params={'history_set': purchases}
        return render(request, 'user-dashboard.html', params)


        a = {'pr9':[5,'Women Keds for Jogging',2000,10000,'http://127.0.0.1:8000/media/shop/images/shoe3_bpwA7Hh.jpg','23/12/2020'],'pr2':[5,'Wrist Band 1',100,500,'http://127.0.0.1:8000/media/shop/images/mensub1_OubvNYp_5Ijt9A9.jpg','23/12/2020']}

        
        # return HttpResponse(h)
        # return HttpResponse(user2.order_history)
    else:
        messages.info(request, 'Please login as ' + uname + ' first')
        return redirect('/accounts/login')



def userEditInfo(request, uname):
    if request.user.is_authenticated and request.user.username == uname:
        user2 = UserCustom.objects.get(username=uname)
        user = User.objects.get(username=uname)
        contactF = user2.contact
        addressF = user2.address
        if request.method == 'POST':
            Ffname = request.POST.get('fname')
            Flname = request.POST.get('lname')
            Fcontact = request.POST.get('contact')
            Femail = request.POST.get('email')
            Faddress = request.POST.get('address')

            user2.address = Faddress
            user2.fname = Ffname
            user2.lname = Flname
            user2.contact = Fcontact
            user2.email = Femail

            user.first_name = Ffname
            user.last_name = Flname
            user.email = Femail

            user.save()
            user2.save()
            messages.info(request, 'Updated user information successfully!')
            return redirect('/accounts/user-dashboard/'+str(uname))

        else:
            params={'contact': contactF, 'address': addressF}
            return render(request, 'user-edit-info.html', params)
    else:
        messages.info(request, 'Please login as ' + uname + ' first')
        return redirect('/accounts/login')


def securitySettings(request, uname):
    if request.user.is_authenticated and request.user.username == uname:
        
        return render(request, 'account-settings.html')
    else:
        messages.info(request, 'Please login as ' + uname + ' first')
        return redirect('/accounts/login')


def deleteUser(request, uname):
    if request.user.is_authenticated and request.user.username == uname:
        user = User.objects.get(username=uname)
        user1 = UserCustom.objects.get(username=uname)
        if request.method == 'POST':
            password = request.POST.get('password')
            if password == user1.password:
                user.delete()
                user1.delete()
                messages.info(request, 'Account deleted successfully')        
                return redirect('/accounts/login')
            else:
                messages.info(request, 'Incorrect Password')        
                return render(request, 'account-settings.html')
        else:    
            return render(request, 'account-settings.html')
    else:
        messages.info(request, 'Please login as ' + uname + ' first')
        return redirect('/accounts/login')



def changePassword(request, uname):
    if request.user.is_authenticated and request.user.username == uname:
        if request.method == 'POST':
            oldPass = request.POST.get('old-password')
            newPass = request.POST.get('new-password')
            newPassConf = request.POST.get('new-password-confirm')

            user2 = User.objects.get(username=uname)
            user3 = UserCustom.objects.get(username=uname)

            if oldPass == user3.password:
                if newPass == newPassConf:
                    user2.set_password(newPass)
                    user3.password = newPass
                    user2.save()
                    user3.save()
                    messages.success(request, 'Successfully changed password!')
                    return redirect('/')
                else:
                    messages.info(request, 'Passwords do not match!')
            else:
                messages.info(request, 'Incorrect Password')
        return render(request, 'account-settings.html')
    else:
        messages.info(request, 'Please login as ' + uname + ' first')
        return redirect('/accounts/login')
    # return HttpResponse(oldPass)


def adminPanel(request):
    categories = Categories.objects.all()
    subcategories = SubCategories.objects.all()
    products = Product.objects.all()
    purchases = Purchases.objects.all()
    discounts = discountedProducts.objects.all()
    users = UserCustom.objects.all()
    advertisements = DiscountAdvertisement.objects.all()
    params  = {'categories': categories, 'discountAdv': advertisements, 'subcategories': subcategories, 'products': products, 'purchases': purchases, 'discounts':discounts, 'users':users}
    return render(request, 'adminPanel.html', params)



def addCategories(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        if Categories.objects.filter(name=name).exists() or Categories.objects.filter(slug=slug).exists():
            messages.info(request, 'The category already exists')
            return redirect('/accounts/adminPanel/addCategories')
        elif ' ' in str(slug):
            messages.info(request, 'Category Names cannot contain spaces, commas or / . Please replace the space by -')
            return redirect('/accounts/adminPanel/addCategories')
        else:
            category = Categories(name=name, slug=slug)
            category.save()
            messages.success(request, 'Successfully added a category')
            return redirect('/accounts/adminPanel')
    return render(request, 'adminAddCategory.html')


def addSubCategories(request, category):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        if SubCategories.objects.filter(name=name, category=category).exists() or SubCategories.objects.filter(slug=slug, category=category).exists():
            messages.info(request, 'The sub-category already exists')
            return redirect('/accounts/adminPanel/addSubCategories/'+category)
        elif ' ' in str(slug):
            messages.info(request, 'Sub Category Names cannot contain spaces, commas or / . Please replace the space by -')
            return redirect('/accounts/adminPanel/addSubCategories/'+category)
        else:
            subcategory = SubCategories(name=name, slug=slug, category=category)
            subcategory.save()
            messages.success(request, 'Successfully added a sub-category')
            return redirect('/accounts/adminPanel')

    return render(request, 'adminAddSubCategory.html', {'category':category})


def addProducts(request, category):
    if request.method == 'POST':
        name = request.POST.get('name')
        subcategory = request.POST.get('SubCategory')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        slug = request.POST.get('slug')
        img = request.FILES.get('img')
        date = datetime.now().strftime('%Y-%m-%d')
        if Product.objects.filter(product_name=name, sub_category=subcategory, category=category).exists() or Product.objects.filter(slug=slug, sub_category=subcategory, category=category).exists():
            messages.info(request, 'A product with a similar name already exists')
            return render(request, 'adminAddProducts.html')
        else:
            add = Product(product_name=name, slug=slug, category=category, sub_category=subcategory, desc=desc, price=price, pub_date=date, image=img, presentPrice=price)
            add.save()
            messages.success(request, 'Successfully added a Product')
            return redirect('/accounts/adminPanel')
    return render(request, 'adminAddProducts.html', {'category':category, 'subcategory': SubCategories.objects.filter(category=category)})


def addDiscount(request, product):
    if discountedProducts.objects.filter(slug=product).exists():
        messages.success(request, 'The product is already in Discounts')
        return redirect('/accounts/adminPanel')
    else:
        if request.method == 'POST':
            discount = request.POST['discount']
            prod = Product.objects.get(slug=product)
            prod.presentPrice = float(prod.price) - float(discount)/100*float(prod.price)
            prod.discount = discount
            entry = discountedProducts(product_name=prod.product_name, product_id=prod.id, category=prod.category, sub_category=prod.sub_category, desc=prod.desc, price=prod.price, pub_date=prod.pub_date, slug=prod.slug, discountPercentage=discount, presentPrice=prod.presentPrice, image=prod.image)
            entry.save()
            prod.save()
        messages.success(request, 'Discount Added to '+ str(prod.product_name))
        return redirect('/accounts/adminPanel')

def addAdv(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        img = request.FILES.get('img')
        date = datetime.now().strftime('%Y-%m-%d')

        add = DiscountAdvertisement(name=name, caption=desc, discountPercentage=price, image=img)
        add.save()
        messages.success(request, 'Successfully added a Advertisement')
        return redirect('/accounts/adminPanel')

    return render(request, 'adminAddAdvertisements.html')

def deleteDiscount(request, product):
    discProd = discountedProducts.objects.get(slug=product)
    prod = Product.objects.get(slug=product)
    prod.discount = 0
    prod.presentPrice = prod.price
    prod.save()
    discProd.delete()
    messages.success(request, 'Removed product from Discounts')
    return redirect('/accounts/adminPanel')


def deleteProducts(request, product):
    prod = Product.objects.get(slug=product)
    prod.delete()
    if discountedProducts.objects.filter(slug=product).exists():
        discountedProducts.objects.get(slug=product).delete()

    messages.success(request, 'Successfully deleted Product')
    return redirect('/accounts/adminPanel')

def deleteAdv(request, product):
    DiscountAdvertisement.objects.get(id=product).delete()
    return redirect('/accounts/adminPanel')