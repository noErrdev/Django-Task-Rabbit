from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from core.models import *


@csrf_exempt
@login_required(login_url="/courier/sign-in/")
def courier_available_jobs_api(request):
    jobs = Job.objects.filter(status=Job.PROCESSING)
    jobs = list(jobs.values())

    return JsonResponse({"success": True, "jobs": jobs})


@csrf_exempt
@login_required(login_url="/courier/sign-in/")
def courier_current_job_update_api(request, pk):
    job = Job.objects.filter(
        id=pk, courier=request.user.courier, status__in=[Job.PICKING, Job.DELIVERING]
    ).last()

    if job.status == Job.PICKING:
        job.pickup_photo = request.FILES["pickup_photo"]
        job.pickedup_at = timezone.now()
        job.status = Job.DELIVERING
        job.save()
        
        try:
            layer = get_channel_layer()
            async_to_sync(layer.group_send)("job_" + str(job.id), {
                "type": "job_update",
                "job": {
                    "status": job.get_status_display(),
                    "pickup_photo": job.pickup_photo.url,
                }
            })
        except Exception:
            pass

    elif job.status == Job.DELIVERING:
        job.delivery_photo = request.FILES["delivery_photo"]
        job.delivered_at = timezone.now()
        job.status = Job.COMPLETED
        job.save()

        try:
            layer = get_channel_layer()
            async_to_sync(layer.group_send)("job_" + str(job.id), {
                "type": "job_update",
                "job": {
                    "status": job.get_status_display(),
                    "delivery_photo": job.delivery_photo.url,
                }
            })
        except Exception:
            pass

    return JsonResponse(
        {
            "success": True,
        }
    )

@csrf_exempt
@login_required(login_url="/courier/sign-in/")
def courier_fcm_token_update_api(request):
    request.user.courier.fcm_token = request.GET.get('fcm_token')
    request.user.courier.save()
    
    return JsonResponse(
        {
            "success": True,
        }
    )