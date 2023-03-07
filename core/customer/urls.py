from django.urls import path
from .views import (
    customer_index,
    customer_profile,
    customer_payment,
    customer_create_job,
    customer_current_jobs,
    customer_archived_jobs,
)

app_name = "customer"

urlpatterns = [
    path("", customer_index, name="home"),
    path("profile/", customer_profile, name="profile"),
    path("payment/", customer_payment, name="payment"),
    path("create-job/", customer_create_job, name="create_job"),
    path("jobs/", customer_current_jobs, name="current_jobs"),
    path("jobs/archived/", customer_archived_jobs, name="archived_jobs"),
]
