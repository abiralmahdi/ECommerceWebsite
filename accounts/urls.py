from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('user-dashboard/<str:uname>', views.userDashboard, name='user-dashboard'),
    path('user-edit-info/<str:uname>', views.userEditInfo, name='user-edit-info'),
    path('security-settings/<str:uname>', views.securitySettings, name='security-settings'),
    path('change-password/<str:uname>', views.changePassword, name='changePassword'),
    path('delete-user/<str:uname>', views.deleteUser, name='deleteAccount'),
    path('adminPanel', views.adminPanel, name='adminPanel'),
    path('adminPanel/addCategories', views.addCategories, name='addCategories'),
    path('adminPanel/addSubCategories/<str:category>', views.addSubCategories, name='addSubCategories'),
    path('adminPanel/addProducts/<str:category>', views.addProducts, name='addSubProducts'),
    path('adminPanel/addAdvertisements', views.addAdv, name='addAdv'),
    path('adminPanel/deleteProducts/<str:product>', views.deleteProducts, name='deleteProducts'),
    path('adminPanel/addDiscount/<str:product>', views.addDiscount, name='addDiscount'),
    path('adminPanel/deleteDiscount/<str:product>', views.deleteDiscount, name='deleteDiscount'),
    path('adminPanel/deleteAdv/<str:product>', views.deleteAdv, name='deleteAdv'),
] 
