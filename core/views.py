from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm

# Create your views here.
def index(request):
    return render(request, "index.html")

@login_required
def customer(request):
    return render(request, "customer.html")

@login_required
def courier(request):
    return render(request, "courier.html")

def sign_up(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
        # Create a new user object but avoid saving it yet
            user = form.save(commit=False)
        # Set the chosen password and email
            user.email = email
            user.set_password(form.cleaned_data['password1'])
        # Save the User object
            user.save()
            return render(request,'signup_done.html',{'user': user})
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})