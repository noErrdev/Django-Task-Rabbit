from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, BasicCustomerForm

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

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
    return render(request, "customer/profile.html", 
        {   "form": form, 
            "customer_form": customer_form, 
            "password_change_form": password_change_form 
        }
    )
