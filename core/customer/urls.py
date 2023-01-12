from django.urls import path 
from .views import customer_index

app_name = "customer"

urlpatterns =  [
    path("", customer_index, name="home"),
]