from django.urls import path
from . import views

app_name = 'adminn'  # Namespace for admin URLs


urlpatterns = [
    #path('products/', views.product_list, name='product_list'),
    #path('addproducts',views.add_product, name='add_product'),
    path('adminhome/',views.adminhome, name='adminhome'),
    path('signout/',views.signout, name='signout'),
    path('users/', views.users, name='users'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('productlist/', views.productlist, name='productlist'),
    path('addvariation/', views.addvariation, name='addvariation'),
    path('variationlist/', views.variationlist, name='variationlist'),
    path('deleteproduct/<int:product_id>/', views.deleteproduct, name = 'deleteproduct'),
    path('editproduct/<int:product_id>/', views.editproduct, name = 'editproduct'),
    path('categorylist/', views.categorylist, name='categorylist'),
    path('addcategory/', views.addcategory, name='addcategory'),
    path('editcategory/<int:category_id>/', views.editcategory, name='editcategory'),
    path('deletecategory/<int:category_id>/', views.deletecategory, name='deletecategory'),
    path('blockuser/<int:user_id>/', views.blockuser, name='blockuser'),
    path('unblockuser/<int:user_id>/', views.unblockuser, name='unblockuser'),
    path('custom_admin_homepage/', views.custom_admin_homepage, name='custom_admin_homepage'),
    
]