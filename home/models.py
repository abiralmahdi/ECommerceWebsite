from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)
    price = models.FloatField(null=True)
    presentPrice = models.FloatField(null=True)
    discount = models.FloatField(null=True)
    pub_date = models.DateField()
    slug = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to='shop/images')
    sellingFrequency = models.CharField(max_length=1000, default=0)

    class Meta:
        ordering = ['-sellingFrequency']

    def __str__(self):
        # return str(self.product_name) + ' || ' + str(self.category)[0:20] + ' ...' + ' || ' + str(self.price) + ' || ' + str(self.pub_date)
        return str(self.product_name) + ' || ' + str(self.category)



class discountedProducts(models.Model):
    product_name = models.CharField(max_length=100)
    product_id = models.CharField(max_length=100, default='')
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)
    discountPercentage = models.FloatField(null=True)
    price = models.FloatField(null=True)
    presentPrice = models.FloatField(null=True)
    pub_date = models.DateField()
    slug = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to='shop/images')
    sellingFrequency = models.CharField(max_length=1000, default=0)

    class Meta:
        ordering = ['-sellingFrequency']

    def __str__(self):
        return str(self.product_name) + ' || ' + str(self.category)
    
class Categories(models.Model):
    name = models.CharField(max_length=1000)
    slug = models.CharField(max_length=1000)
    def __str__(self):
        return str(self.name) + ' || ' + str(self.slug)


class Purchases(models.Model):
    product_details = models.CharField(max_length=99999999999999)
    customerUsername = models.CharField(max_length=1000)
    totalPrice = models.CharField(max_length=1000)
    discount = models.CharField(max_length=1000)
    dates = models.CharField(max_length=1000)
    def __str__(self):
        return str(self.customerUsername) + ' || '


class SubCategories(models.Model):
    name = models.CharField(max_length=1000)
    slug = models.CharField(max_length=1000)
    category = models.CharField(max_length=1000)
    def __str__(self):
        return str(self.name) + ' || ' + str(self.category)

class Advertisements(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)
    price = models.CharField(max_length=10)
    pub_date = models.DateField()
    slug = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to='shop/images')

    def __str__(self):
        # return str(self.product_name) + ' || ' + str(self.category)[0:20] + ' ...' + ' || ' + str(self.price) + ' || ' + str(self.pub_date)
        return str(self.product_name) + ' || ' + str(self.category)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    message = models.CharField(max_length=700)
    # datemsg = models.DateField()


    def __str__(self):
        return str(self.name) + ' || ' + str(self.email) + ' || ' + str(self.contact) + ' || '


class UserCustom(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    no_of_orders = models.CharField(max_length=100)

    def __str__(self):
        return str(self.fname) + ' || ' + str(self.email) + ' || ' + str(self.username) + ' || '

class DiscountAdvertisement(models.Model):
    name = models.CharField(max_length=500, null=True)
    caption = models.CharField(max_length=1000, null=True)
    image = models.ImageField(upload_to='shop/images')
    discountPercentage = models.FloatField(null=True)

    def __str__(self):
        return str(self.name)

class Comments(models.Model):
    userName = models.CharField(max_length=1000)
    userID = models.CharField(max_length=1000)
    productID = models.CharField(max_length=1000)
    dateTime = models.CharField(max_length=1000)
    comment = models.CharField(max_length=100000)

    def __str__(self):
        return str(self.name)


        