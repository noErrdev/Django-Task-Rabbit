from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, BasicCustomerForm

@login_required
def customer_index(request):
    return redirect(reverse('customer:profile'))

@login_required(login_url="/sign-in/?next=/customer/")
def customer_profile(request):
    form = UserProfileForm(instance=request.user)
    customer_form = BasicCustomerForm(instance=request.user.customer)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        customer_form = BasicCustomerForm(request.POST, request.FILES, instance=request.user.customer)
        if form.is_valid() and customer_form.is_valid():
            form.save()
            customer_form.save()
            return redirect(reverse('customer:profile'))
    return render(request, "customer/profile.html", { "form": form, "customer_form": customer_form })
