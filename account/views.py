from urllib import request
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import CreateUserForm, LoginForm, UpdateUserForm
from .token import user_tokenizer_generate
from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order, OrderItem



def register(request):
    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            user.is_active = False
            user.save()
            
            current_site = get_current_site(request)
            
            subject = 'Account verification'
            message = render_to_string('account/registration/email-verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),
            })
            
            user.email_user(subject=subject, message=message)
            
            return redirect('email_verification_sent')
            
            
        
    context = {'form': form}
             
           
    return render(request, 'account/registration/register.html', context=context)



def account(request):
    return render(request, 'account/account.html')



def email_verification(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        
        user.save()
        
        return redirect('email_verification_success')
    
    else:
        return redirect('email_verification_failed')



def email_verification_sent(request):
    return render(request, 'account/registration/email-verification-sent.html')



def email_verification_success(request):
    return render(request, 'account/registration/email-verification-success.html')



def email_verification_failed(request):
    return render(request, 'account/registration/email-verification-failed.html')



def my_login(request):
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username= request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth.login(request, user)
                
                return redirect('dashboard')
    context = {'form': form}
    
    return render(request, 'account/my-login.html', context=context)



def user_logout(request):
    
    try:
        for key in list(request.session.keys()):
            if key == 'session_key':
                continue
            else:
                del request.session[key]
    except KeyError:
        pass
    
    messages.success(request, 'You have been logged out')
    
    return redirect('store')



@login_required(login_url='my_login')
def dashboard(request):
    return render(request, 'account/dashboard.html')



@login_required(login_url='my_login')
def profile(request):
    user_form = UpdateUserForm(instance=request.user)
    
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        
        if user_form.is_valid():
            user_form = user_form.save()
            
            messages.info(request, 'Account updated successfully')
            return redirect('dashboard')
        
       
    context = {'user_form': user_form}
    
    return render(request, 'account/profile.html', context=context)



@login_required(login_url='my_login')
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        user.delete()
        messages.error(request, 'Account deleted successfully')
        return redirect('store')
    
    
    return render(request, 'account/delete-account.html')



@login_required(login_url='my_login')
def manage_shipping(request):
    try:
        shipping = ShippingAddress.objects.get(user=request.user.id)
    except ShippingAddress.DoesNotExist:
        shipping = None
        
    form = ShippingForm(instance=shipping)
    
    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=shipping)
        
        if form.is_valid():
            shipping_user = form.save(commit=False)
            shipping_user.user = request.user
            shipping_user.save()
            
            return redirect('dashboard')
        
    context = {'form': form}
    
    return render(request, 'account/manage-shipping.html', context=context)



@login_required(login_url='my-login')
def track_orders(request):
    try:
        orders = OrderItem.objects.filter(user=request.user)
        
        context = {'orders': orders,}
        
        return render(request, 'account/track-orders.html', context=context)
    except:
          
        return render(request, 'account/track-orders.html')
