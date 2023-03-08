from django.urls import path 
from .views import courier_index, courier_available_jobs

app_name = "courier"

urlpatterns =  [
    path("", courier_index, name="home"),
    path("jobs/", courier_available_jobs, name="available_jobs"),
]