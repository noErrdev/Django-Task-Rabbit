from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def customer_index(request):
    return render(request, "customer.html")
