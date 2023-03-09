from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.models import *

available_jobs_namespace = "courier:available_jobs"


@login_required(login_url="/sign-in/?next=/courier/")
def courier_index(request):
    return redirect(reverse(available_jobs_namespace))


@login_required(login_url="/sign-in/?next=/courier/")
def courier_available_jobs(request):
    return render(request, "courier/available-jobs.html")


@login_required(login_url="/sign-in/?next=/courier/")
def courier_available_job(request, pk):
    job = Job.objects.filter(id=pk, status=Job.PROCESSING).last()

    if not job:
        return redirect(reverse(available_jobs_namespace))
    if request.method == "POST":
        job.courier = request.user.courier
        job.status = Job.PICKING
        job.save()
        return redirect(reverse(available_jobs_namespace))
    return render(request, "courier/available-job-details.html", {"job": job})


@login_required(login_url="/sign-in/?next=/courier/")
def courier_current_job(request):
    job = Job.objects.filter(
        courier=request.user.courier, status__in=[Job.PICKING, Job.DELIVERING]
    ).last()
    return render(request, "courier/current-job.html", {"job": job})


@login_required(login_url="/sign-in/?next=/courier/")
def courier_current_job_camera(request, pk):
    job = Job.objects.filter(
        id=pk, courier=request.user.courier, status__in=[Job.PICKING, Job.DELIVERING]
    ).last()
    if not job:
        return redirect(reverse("courier:current_job"))
    return render(request, "courier/current-job-take-photo.html", {"job": job})


@login_required(login_url="/sign-in/?next=/courier/")
def courier_job_completed(request):
    return render(request, "courier/completed-job.html")
