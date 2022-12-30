from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")

def customer(request):
    return render(request, "customer.html")

def courier(request):
    return render(request, "courier.html")