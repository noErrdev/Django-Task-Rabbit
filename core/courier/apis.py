from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from core.models import *

@csrf_exempt
@login_required(login_url="/sign-in/courier/")
def courier_available_jobs_api(request):
    jobs = Job.objects.filter(status=Job.PROCESSING)
    jobs = list(jobs.values())

    return JsonResponse({
        "sucess": True,
        "jobs": jobs
    })
