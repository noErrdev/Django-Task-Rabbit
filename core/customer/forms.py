from django import forms
from django.contrib.auth.models import User

from core.models import Customer, Job

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]

class BasicCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("avatar",)

class JobCreationForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["name", "description", "category", "size", "quantity", "photo"]

class JobPickupForm(forms.ModelForm):
    pickup_address = forms.CharField(required=True)
    pickup_name = forms.CharField(required=True)
    pickup_phone_number = forms.CharField(required=True)
    
    class Meta:
        model = Job
        fields = ["pickup_address", "pickup_latitude", "pickup_longtitude", "pickup_name", "pickup_phone_number"]