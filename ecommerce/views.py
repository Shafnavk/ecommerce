from django.shortcuts import get_object_or_404, render
from store.models import Product

def home(request):
    Products = Product.objects.all().filter(is_available=True)

    context = {
        'products' : Products,
    }
    return render(request, 'home.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})

