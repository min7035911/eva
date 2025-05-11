# home/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home_index"),
    path('search/', views.product_search, name='product_search'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms-and-conditions'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
]
