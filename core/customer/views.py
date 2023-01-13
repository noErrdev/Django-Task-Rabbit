from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import CustomerProfileForm

@login_required
def customer_index(request):
    return redirect(reverse('customer:profile'))

@login_required(login_url="/sign-in/?next=/customer/")
def customer_profile(request):
    form = CustomerProfileForm(instance=request.user)

    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('customer:profile'))
    return render(request, "customer/profile.html", { "form": form })
