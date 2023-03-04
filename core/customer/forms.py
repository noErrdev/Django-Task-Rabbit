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