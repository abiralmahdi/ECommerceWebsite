from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us', views.home, name='about'),
    path('products/sub-categories/<str:category>/<str:sub_category>', views.subAllProducts, name='subAllProducts'),
    path('products/<str:category>', views.allProducts, name='allProducts'),
    path('products/<str:category>/<str:ids>', views.indivProduct, name='IndivProducts'),
    path('addComment/<str:category>/<str:ids>', views.addComment, name='Comment'),
    path('discountedProducts/', views.discountProducts, name='discountedProducts'),
    path('discountedIndivProducts/<str:productID>', views.discountIndivProducts, name='discountedindivProducts'),
    path('contact-us', views.contact, name='contact'),
    path('search', views.search, name='search'),
    # path('cart_detail', views.cart, name='cart'),
    # path('add_to_cart/<str:ids>', views.add_to_cart, name='add_to_cart'),
    # path('delete_from_cart/<str:ids>', views.delete_from_cart, name='delete_from_cart'),
    # path('clearCart', views.clear_cart, name='delete_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment', views.payment, name='payment'),
    path('completeOrder/<str:username1>', views.completeOrder, name='completeOrder'),
    path('incompleteOrder/<str:username1>', views.incompleteOrder, name='incompleteOrder'),
    

    
    
    

]
