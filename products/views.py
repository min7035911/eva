from django.shortcuts import render, get_object_or_404
from .models import CarBrand, CarModel, FloorMatProduct

def brand_list(request):
    brands = CarBrand.objects.all()
    return render(request, 'products/brand_list.html', {'brands': brands})

def model_list(request, brand_slug):
    brand = get_object_or_404(CarBrand, slug=brand_slug)
    models = brand.models.all()
    return render(request, 'products/model_list.html', {'brand': brand, 'models': models})

def product_detail(request, pk):
    product = get_object_or_404(FloorMatProduct, pk=pk)
    return render(request, 'products/product.html', {'product': product})
