from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from core.models import *


@csrf_exempt
@login_required(login_url="/sign-in/courier/")
def courier_available_jobs_api(request):
    jobs = Job.objects.filter(status=Job.PROCESSING)
    jobs = list(jobs.values())

    return JsonResponse({"success": True, "jobs": jobs})


@csrf_exempt
@login_required(login_url="/sign-in/courier/")
def courier_current_job_update_api(request, pk):
    job = Job.objects.filter(
        id=pk, courier=request.user.courier, status__in=[Job.PICKING, Job.DELIVERING]
    ).last()

    if job.status == Job.PICKING:
        job.pickup_photo = request.FILES["pickup_photo"]
        job.pickedup_at = timezone.now()
        job.status = Job.DELIVERING
        job.save()
    elif job.status == Job.DELIVERING:
        job.delivery_photo = request.FILES["delivery_photo"]
        job.delivered_at = timezone.now()
        job.status = Job.COMPLETED
        job.save()

    return JsonResponse(
        {
            "success": True,
        }
    )
