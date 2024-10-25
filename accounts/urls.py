
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path("login/google",views.login_with_google,name="google_login"),
    path("google/login/callback/",views.google_callback,name="google_callback"),
    path('login_customer/', views.login, name='login'),
    path('login_admin/', views.loginn, name='loginn'),
    path('logout_customer/', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword', views.resetPassword, name='resetPassword'),


]
