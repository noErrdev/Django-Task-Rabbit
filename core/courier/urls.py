from django.urls import path 
from .views import courier_index

app_name = "courier"

urlpatterns =  [
    path("", courier_index, name="home"),
]