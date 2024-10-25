from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views  # Ensure product_detail is in views

urlpatterns = [
    path('dj-admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('adminn/', include('adminn.urls', namespace='adminn')),
    path('', views.home, name='home'),
    path('store/', include('store.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
