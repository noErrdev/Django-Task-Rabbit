from django.urls import path 
from .views import customer_index, customer_profile

app_name = "customer"

urlpatterns =  [
    path("", customer_index, name="home"),
    path("profile/", customer_profile, name="profile")
]