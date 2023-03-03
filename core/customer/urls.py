from django.urls import path 
from .views import customer_index, customer_profile, customer_payment

app_name = "customer"

urlpatterns =  [
    path("", customer_index, name="home"),
    path("profile/", customer_profile, name="profile"),
    path("payment/", customer_payment, name="payment")
]