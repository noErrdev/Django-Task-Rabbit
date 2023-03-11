from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/jobs/<str:job_id>/", consumers.JobConsumer.as_asgi()),
]