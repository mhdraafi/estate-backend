from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register/', views.register),
    path('login/', views.login),
    path('properties/', views.property_list),
    path('properties/<int:pk>/', views.property_detail),  
    path('enquiries/', views.enquiry),
    path('contact/', views.contact_message, name='contact'),
    path('cart/', views.cart_list),              
    path('cart/add/', views.add_to_cart),       
    path('cart/remove/<int:pk>/', views.remove_from_cart),
    path('users/', views.user_list),
]

