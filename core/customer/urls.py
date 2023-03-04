from django.urls import path 
from .views import customer_index, customer_profile, customer_payment, customer_create_job

app_name = "customer"

urlpatterns =  [
    path("", customer_index, name="home"),
    path("profile/", customer_profile, name="profile"),
    path("payment/", customer_payment, name="payment"),
    path("create_job/", customer_create_job, name="create_job")
]