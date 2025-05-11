from django.urls import path
from . import views

urlpatterns = [
    path('brands/', views.brand_list, name='brand_list'),
    path('brands/<slug:brand_slug>/models/', views.model_list, name='model_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
