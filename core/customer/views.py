from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, BasicCustomerForm

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

import firebase_admin
from firebase_admin import credentials, auth

if settings.DEBUG == True:
    cred = credentials.Certificate(settings.FIREBASE_ADMIN_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
elif settings.DEBUG == False:
    cred = credentials.Certificate(settings.FIREBASE_ADMIN_CREDENTIALS_DICT)
    firebase_admin.initialize_app(cred)

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

profile_namespace = 'customer:profile'

@login_required
def customer_index(request):
    return redirect(reverse(profile_namespace))

@login_required(login_url="/sign-in/?next=/customer/")
def customer_profile(request):
    form = UserProfileForm(instance=request.user)
    customer_form = BasicCustomerForm(instance=request.user.customer)
    password_change_form = PasswordChangeForm(request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        customer_form = BasicCustomerForm(request.POST, request.FILES, instance=request.user.customer)
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if request.POST.get('action') == 'update_profile':
            if form.is_valid() and customer_form.is_valid():
                form.save()
                customer_form.save()
                messages.success(request, "Your profile has been updated sucessfully!")
                return redirect(reverse(profile_namespace))
        elif request.POST.get('action') == 'update_password':
            if password_change_form.is_valid(): 
                user_password = password_change_form.save()
                update_session_auth_hash(request, user_password)
                messages.success(request, "Your password has been updated sucessfully!")
                return redirect(reverse(profile_namespace))
        elif request.POST.get('action') == 'update_phone':
            firebase_user = auth.verify_id_token(request.POST.get('id_token'))
            request.user.customer.phone_number = firebase_user['phone_number']
            request.user.customer.save()
            return redirect(reverse(profile_namespace))
    return render(request, "customer/profile.html", 
        {   "form": form, 
            "customer_form": customer_form, 
            "password_change_form": password_change_form 
        }
    )

@login_required(login_url="/sign-in/?next=/customer/")
def customer_payment(request):
    current_customer = request.user.customer
    if not current_customer.stripe_customer_id:
        customer = stripe.Customer.create()
        current_customer.stripe_customer_id = customer['id']
        current_customer.save()
    
    intent = stripe.SetupIntent.create(
        customer=current_customer.stripe_customer_id,
        payment_method_types=["card"],
    )
    return render(request, "customer/payment.html", { "client_secret": intent.client_secret })