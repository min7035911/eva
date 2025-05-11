# home/views.py

from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from products.models import FloorMatProduct, CarBrand


def index(request):
    """
    Главная страница: список ковриков с фильтром по марке и сортировкой.
    """
    qs = FloorMatProduct.objects.all()
    brands = CarBrand.objects.all()
    selected_brand = request.GET.get('category')
    selected_sort = request.GET.get('sort')

    # Фильтрация по марке (slug)
    if selected_brand:
        qs = qs.filter(car_model__brand__slug=selected_brand)

    # Сортировка
    if selected_sort:
        if selected_sort == 'newest':
            qs = qs.order_by('-created')
        elif selected_sort == 'priceAsc':
            qs = qs.order_by('price')
        elif selected_sort == 'priceDesc':
            qs = qs.order_by('-price')

    # Пагинация — 20 штук на страницу
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 20)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'home/index.html', {
        'products': products,
        'brands': brands,
        'selected_brand': selected_brand,
        'selected_sort': selected_sort,
    })


def product_search(request):
    """
    Поиск ковриков по части названия.
    """
    query = request.GET.get('q', '').strip()
    if query:
        products = FloorMatProduct.objects.filter(
            Q(name__icontains=query) | Q(name__istartswith=query)
        )
    else:
        products = FloorMatProduct.objects.none()

    return render(request, 'home/search.html', {
        'query': query,
        'products': products,
    })


def contact(request):
    return render(request, 'home/contact.html', {"form_id": "xgvvlrvn"})


def about(request):
    return render(request, 'home/about.html')


def terms_and_conditions(request):
    return render(request, 'home/terms_and_conditions.html')


def privacy_policy(request):
    return render(request, 'home/privacy_policy.html')
