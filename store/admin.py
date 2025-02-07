from django.contrib import admin
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'price', 'stock', 'is_available', 'created_date', 'modified_date')
    list_filter = ('is_available', 'created_date', 'modified_date', 'category')
    list_editable = ('price', 'stock', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

admin.site.register(Product, ProductAdmin)

