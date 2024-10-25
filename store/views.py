
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Product, Category
from django.db.models import Q

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True)
        product_count = products.count()
    
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        # Correctly filter using both category_slug and product_slug
        single_product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):


    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            # Use Q objects to search in both description and product_name fields
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
            product_count = products.count()

    context = {
        'products': products,
        'product_count' : product_count,
    }
    return render(request, 'store/store.html', context)