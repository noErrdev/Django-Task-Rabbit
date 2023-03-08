from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

available_jobs_namespace = 'courier:available_jobs'

@login_required(login_url="/sign-in/?next=/courier/")
def courier_index(request):
    return redirect(reverse(available_jobs_namespace))

@login_required(login_url="/sign-in/?next=/courier/")
def courier_available_jobs(request):
    return render(request, "courier/available-jobs.html")

