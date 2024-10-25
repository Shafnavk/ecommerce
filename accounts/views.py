import secrets
from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from .models import Account  # Ensure this points to your custom user model
from .forms import RegistrationForm
from django.urls import reverse

from django.contrib.sites.shortcuts import get_current_site 
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, send_mail

# Create your views here.

def register(request):
    if request.method == 'POST':  # Corrected case
        form = RegistrationForm(request.POST)  # Corrected POST
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name = first_name, last_name= last_name, email= email, username = username, password = password)
            user.phone_number = phone_number
            user.save()
            

            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Registration successful. Please check your email to activate your account.')
            return redirect('accounts/login')
    else:    
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate user
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)  # Pass the authenticated user object
            messages.success(request, 'Logged in successfully')
            return redirect('home')  # Redirect to home or another page
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')  # Reload login page on failure

    return render(request, 'accounts/login.html')



def activate(request, uidb64, token):
    try:
        # Decode the user ID from the base64-encoded string
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid) 
        
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # Check if the token is valid and activate the user if so
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Activate the user
        user.save()  # Save the user object
        messages.success(request, 'Your account has been activated! You can now log in.')
        return redirect('login')  # Redirect to the login page after activation
    else:
        messages.error('Activation link is invalid!')
        return redirect('register')
    
@login_required(login_url='login')  # Ensures user must be logged in to log out
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out.')
    
    # Redirect the user to the login page (or another page if preferred)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    return render (request, 'accounts/dashboard.html')

def forgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')  # Use get() to fetch the email from the form
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Prepare email
            current_site = get_current_site(request)
            mail_subject = 'Reset Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('login')  # Redirect to login after email is sent

        else:
            messages.error(request, 'Account with that email does not exist.')

    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request):
    return HttpResponse('ok')


def resetpassword_validate(request, uidb64, token):
    try: 
        uid  = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist): user - None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request,'Please reset your password') 
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!') 
        return redirect('login')
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid= request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successfull')
            return redirect('login') 
        else:
            messages.error(request,'Password do not match')
            return redirect('resetPassword')
    else:
        return render(request,'accounts/resetPassword.html')
    
def loginn(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart) 

                    # getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    #Get the cart items from the user to access his product variation
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    #product_variation = [1, 2, 3, 4, 6]
                    #ex_var_list = [4, 6, 3, 5]
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                pass

            auth.login(request, user)
            #messages.success(request, 'You are now logged in')
            if user.is_superadmin:
                # Redirect superuser to admin home 
                return redirect('adminn:adminhome')
            else:
                # Redirect regular user to user home
                messages.success(request, 'You are now logged in')
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    #next=/cart/checkout/
                    params = dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                        nextPage = params['next']
                        return redirect(nextPage)
                    
                except:
                    return redirect('dashboard')
        else:
            messages.error(request, "Invalid Login Credentials")
            return redirect('loginn')
    return render(request, 'accounts/loginn.html')

def login_with_google(request):
    google_client_id = settings.GOOGLE_CLIENT_ID
    redirect_uri = request.build_absolute_uri(reverse('google_callback'))
    scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
    state = secrets.token_urlsafe(16)
    request.session['oauth_token'] = state

    params ={
        'client_id': google_client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': scope,
        'state': state,
        'access_type': 'offline',
        'prompt': 'select_account'
    }
    url = f'https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}'
    return redirect(url)


def google_callback(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        state = request.GET.get('state')
        error = request.GET.get('error')
        session_state = request.session.get('oauth_token')
        request.session.pop('oauth_token',None)
        if error or not state or state != session_state: 
            messages.error(request, f"Not Authenticated")
            return redirect('loginn')
        token_url =  "https://oauth2.googleapis.com/token"
        token_data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': request.build_absolute_uri(reverse('google_callback')),
            'grant_type': 'authorization_code'
        }
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        access_token = token_json.get('access_token')


        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        user_info_params = {"access_token": access_token}
        user_info_response = requests.get(user_info_url, params=user_info_params)
        user_info = user_info_response.json()

        email = user_info.get('email')
        full_name  = user_info.get('name')
        first_name = full_name.split(' ')[0]
        last_name = full_name.split(' ')[-1]
        username = email.split('@')[0]

        user , created = user.objects.get_or_create(email=email,defaults={
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'is_active': True,
        })
        if created:
            user.set_unusable_password()
            user.save()
        auth.login(request, user)
        messages.success(request, f"Login Successful with Google")
        return redirect('user_home')

   