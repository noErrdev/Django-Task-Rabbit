from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.models import Job
from .forms import PaymentForm

available_jobs_namespace = "courier:available_jobs"


@login_required(login_url="/sign-in/?next=/courier/")
def courier_index(request):
    return redirect(reverse(available_jobs_namespace))


@login_required(login_url="/sign-in/?next=/courier/")
def courier_profile(request):
    jobs = Job.objects.filter(courier=request.user.courier, status=Job.COMPLETED)
    total_earnings = sum(job.price for job in jobs) * 0.7
    total_earnings = round(total_earnings, 2)
    total_jobs = len(jobs)
    total_distance = sum(job.distance for job in jobs)
    return render(
        request,
        "courier/profile.html",
        {
            "jobs": jobs,
            "total_earnings": total_earnings,
            "total_jobs": total_jobs,
            "total_distance": total_distance,
        },
    )


@login_required(login_url="/sign-in/?next=/courier/")
def courier_payment_method(request):
    payment_form = PaymentForm(instance=request.user.courier)

    if request.method == "POST":
        payment_form = PaymentForm(request.POST, instance=request.user.courier)
        if payment_form.is_valid():
            payment_form.save()
            messages.success(
                request, "Your payment email has been successfully updated!"
            )
            return redirect(reverse("courier:profile"))
    return render(request, "courier/payment.html", {"payment_form": payment_form})


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


@login_required(login_url="/sign-in/?next=/courier/")
def courier_archived_jobs(request):
    jobs = Job.objects.filter(courier=request.user.courier, status=Job.COMPLETED)
    return render(request, "courier/archived-jobs.html", {"jobs": jobs})
