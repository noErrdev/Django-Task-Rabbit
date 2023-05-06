"""
taskrabbit URL Configuration
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from core.views import index, sign_up
import core.customer.urls
import core.courier.urls

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("sign-in/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("sign-up", sign_up, name="sign_up"),
    path('accounts/', include('allauth.urls')),
    path("customer/", include(core.customer.urls, namespace="customer")),
    path("courier/", include(core.courier.urls, namespace="courier")),
    path(
        "firebase-messaging-sw.js",
        (
            TemplateView.as_view(
                template_name="firebase-messaging-sw.js",
                content_type="application/x-javascript",
            )
        ),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
