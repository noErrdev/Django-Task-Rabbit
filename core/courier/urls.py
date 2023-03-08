from django.urls import path 
from .views import courier_index, courier_available_jobs
from .apis import courier_available_jobs_api

app_name = "courier"

urlpatterns =  [
    path("", courier_index, name="home"),
    path("jobs/", courier_available_jobs, name="available_jobs"),
    path("api/jobs/", courier_available_jobs_api, name="available_jobs_api"),
]