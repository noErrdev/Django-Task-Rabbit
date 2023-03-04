import uuid
from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='customer/avatars/', blank=True , null=True)
    phone_number = models.CharField(max_length=50, blank=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_payments_method_id = models.CharField(max_length=255, blank=True)
    stripe_card_last_4_digits = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name()
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    SIZES = (
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    )

    JOB_STATUS = (
        ('creating', 'Creating'),
        ('processing', 'Processing'),
        ('picking', 'Picking'),
        ('delivering', 'Delivering'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.CharField(max_length=6, choices=SIZES, default="medium")
    status = models.CharField(max_length=10, choices=JOB_STATUS, default="creating")
    quantity = models.IntegerField(default=1)
    photo = models.ImageField(upload_to='job/photos/')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name


