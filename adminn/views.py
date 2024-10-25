
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import csv
from django.contrib import messages,auth
from django.db.models.functions import Coalesce
from .utils import is_ajax
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.template.loader import render_to_string
from accounts.models import Account
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404
from .forms import ProductForm, ProductImageForm,  VariationForm
from store.models import Product, ProductImage,Variation
from .forms import CategoryForm
from django.db.models import Sum, Count, F
from django.db.models.functions import ExtractWeek, ExtractMonth
from category.models import Category
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Sum, Q
from datetime import timedelta, date
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from io import BytesIO
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseBadRequest


# Create your views here.

def superuser_required(view_func):
    """
    Decorator for views that checks if the user is a superuser,
    redirects to the dashboard if not.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superadmin:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('loginn')  # Redirect to the dashboard or any other page
    return _wrapped_view

def user_view(request):
    return render(request, 'customer/home.html')

@superuser_required
def adminhome(request):
    # Render your custom admin panel homepage template
    return render(request, 'adminn/adminhome.html')  

@superuser_required
def users(request):
    # Fetch account objects from the database
    accounts = Account.objects.all()  # You can filter or order the queryset as needed
    
    # Pass the accounts queryset to the template context
    context = {'accounts': accounts}
    
    # Render the template with the context
    return render(request, 'adminn/users.html', context)

@superuser_required
def signout(request):
    auth.logout(request)
    messages.success(request, "you are logged out")
    return redirect('loginn')


def addproduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        form_image = ProductImageForm(request.POST, request.FILES)
        if form.is_valid() and form_image.is_valid():
            product = form.save()
            images = request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            return redirect('success_url')  # Replace with your actual success URL
    else:
        form = ProductForm()
        form_image = ProductImageForm()

    context = {
        'form': form,
        'form_image': form_image,
    }
    return render(request, 'adminn/addproduct.html', context)

@superuser_required
def productlist(request):
    products = Product.objects.all()
    return render(request, 'adminn/productlist.html', {'products': products})

def deleteproduct(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_active = False
    product.save()
    return redirect('adminn:productlist')

def editproduct(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(instance=product)
    image_form = ProductImageForm()
    
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        image_form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid() and image_form.is_valid():
            form.save()
            
            if 'images' in request.FILES:
                for image in request.FILES.getlist('images'):
    
                    ProductImage.objects.create(product=product, image=image)
            messages.success(request, "Product edited successfully")
            return redirect("adminn:productlist")
        else:
            messages.error(request, "Error editing product. Please check the form.")
    else:
        # This ensures existing images can be seen and edited
        image_form = ProductImageForm(initial={'images': product.images.all()})
    # Fetch existing images and pass them to the template
    existing_images = product.images.all()
    return render(request, "adminn/editproduct.html", {"form": form, "image_form": image_form, "existing_images": existing_images })

@superuser_required
def addvariation(request):
    if request.method == 'POST':
        form = VariationForm(request.POST)
        if form.is_valid():
            variation = form.save(commit=False)
            variation.save()
            return redirect('adminn:variationlist')  # Redirect to the variation list page
    else:
        form = VariationForm()
    return render(request, 'adminn/addvariation.html', {'form': form})

@superuser_required
def variationlist(request):
    variations = Variation.objects.all()
    return render(request, 'adminn/variationlist.html', {'variations': variations})

@superuser_required
def categorylist(request):
    categories = Category.objects.all()
    return render(request, 'adminn/categorylist.html', {'categories': categories})

def addcategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminn:categorylist')
    else:
        form = CategoryForm()
    return render(request, 'adminn/addcategory.html', {'form': form})

def editcategory(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('adminn:categorylist')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'adminn/editcategory.html', {'form': form})

def deletecategory(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    # Soft delete all products associated with the category
    products_to_delete = Product.objects.filter(category=category)
    products_to_delete.update(is_active=False)
    
    # Deactivate the category
    category.is_active = False
    category.save()# Update the 'is_active' field to False instead of deleting
    return redirect('adminn:categorylist')

def blockuser(request, user_id):
    # Retrieve the user object by its id
    account = Account.objects.get(id=user_id)
    
    # Block the user (set is_active to False)
    account.is_active = False
    account.save()
    
    # Redirect back to the user list page or any other appropriate page
    return redirect('adminn:users')  

def unblockuser(request, user_id):
    # Retrieve the user object by its id
    account = Account.objects.get(id=user_id)
    
    # Unblock the user (set is_active to True)
    account.is_active = True
    account.save()
    
    # Redirect back to the user list page or any other appropriate page
    return redirect('adminn:users') 



@superuser_required
def custom_admin_homepage(request):
    filter_period = 'yearly'
    today = timezone.now().date()

    if request.method == 'POST':
        if 'period' in request.POST:
            filter_period = request.POST['period']
        
   

