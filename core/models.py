import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="customer/avatars/", blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_payments_method_id = models.CharField(max_length=255, blank=True)
    stripe_card_last_4_digits = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Courier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=300, blank=True, default="courier address")
    latitude = models.FloatField(blank=True, default=0)
    longtitude = models.FloatField(blank=True, default=0)

    def __str__(self):
        return self.user.get_full_name()


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

    SIZES = (
        (SMALL, "Small"),
        (MEDIUM, "Medium"),
        (LARGE, "Large"),
    )

    CREATING = "creating"
    PROCESSING = "processing"
    PICKING = "picking"
    DELIVERING = "delivering"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    JOB_STATUS = (
        (CREATING, "Creating"),
        (PROCESSING, "Processing"),
        (PICKING, "Picking"),
        (DELIVERING, "Delivering"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    courier = models.ForeignKey(
        Courier, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=300)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    size = models.CharField(max_length=6, choices=SIZES, default=MEDIUM)
    status = models.CharField(max_length=10, choices=JOB_STATUS, default=CREATING)
    quantity = models.IntegerField(default=1)
    photo = models.ImageField(upload_to="job/photos/")
    created_at = models.DateTimeField(default=timezone.now)

    pickup_address = models.CharField(max_length=300, blank=True, default="job address")
    pickup_latitude = models.FloatField(default=0, blank=True, null=True)
    pickup_longtitude = models.FloatField(default=0, blank=True, null=True)
    pickup_name = models.CharField(max_length=300, blank=True)
    pickup_phone_number = models.CharField(max_length=50, blank=True)

    delivery_address = models.CharField(
        max_length=300, blank=True, default="delivery address"
    )
    delivery_latitude = models.FloatField(default=0, blank=True, null=True)
    delivery_longtitude = models.FloatField(default=0, blank=True, null=True)
    delivery_name = models.CharField(max_length=300, blank=True)
    delivery_phone_number = models.CharField(max_length=50, blank=True)

    duration = models.IntegerField(default=0)
    distance = models.FloatField(default=0)
    price = models.FloatField(default=0)

    pickup_photo = models.ImageField(
        upload_to="job/pickup_photos/", null=True, blank=True
    )
    pickedup_at = models.DateTimeField(null=True, blank=True)

    delivery_photo = models.ImageField(
        upload_to="job/delivery_photos/", null=True, blank=True
    )
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.description

    def get_status_display(self):
        return self.status

    def get_size_display(self):
        return self.size.capitalize()

    def get_absolute_url(self):
        return reverse("customer:job_details", kwargs={"pk": self.pk})


class Transaction(models.Model):
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.stripe_payment_intent_id
