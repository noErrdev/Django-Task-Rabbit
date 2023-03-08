from django.urls import path 
from .views import courier_index, courier_available_jobs, courier_available_job, courier_current_job
from .apis import courier_available_jobs_api

app_name = "courier"

urlpatterns =  [
    path("", courier_index, name="home"),
    path("jobs/", courier_available_jobs, name="available_jobs"),
    path("jobs/current/", courier_current_job, name="current_job"),
    path("jobs/<str:pk>/", courier_available_job, name="available_job_details"),
    path("api/jobs/", courier_available_jobs_api, name="available_jobs_api"),
]