from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string


@receiver(post_save, sender=User)
def send_welcome_mail(sender, instance, created, **kwargs):
    if created and instance.email:
        body = render_to_string(
            "welcome_email.html", {"name": instance.get_full_name()}
        )
        send_mail(
            "Welcome to Task Rabbit",
            body,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=True,
        )
