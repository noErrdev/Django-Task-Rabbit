import requests
import stripe
import firebase_admin

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import (
    UserProfileForm,
    BasicCustomerForm,
    JobCreationForm,
    JobPickupForm,
    JobDeliveryForm,
)
from ..models import Job, Transaction

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from firebase_admin import credentials, auth

if settings.DEBUG == True:
    cred = credentials.Certificate(settings.FIREBASE_ADMIN_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
elif settings.DEBUG == False:
    cred = credentials.Certificate(settings.FIREBASE_ADMIN_CREDENTIALS_DICT)
    firebase_admin.initialize_app(cred)


stripe.api_key = settings.STRIPE_SECRET_KEY


profile_namespace = "customer:profile"
create_job_namespace = "customer:create_job"


@login_required
def customer_index(request):
    return redirect(reverse(profile_namespace))


@login_required(login_url="/sign-in/?next=/customer/")
def customer_profile(request):
    form = UserProfileForm(instance=request.user)
    customer_form = BasicCustomerForm(instance=request.user.customer)
    password_change_form = PasswordChangeForm(request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        customer_form = BasicCustomerForm(
            request.POST, request.FILES, instance=request.user.customer
        )
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if request.POST.get("action") == "update_profile":
            if form.is_valid() and customer_form.is_valid():
                form.save()
                customer_form.save()
                messages.success(request, "Your profile has been updated sucessfully!")
                return redirect(reverse(profile_namespace))
        elif request.POST.get("action") == "update_password":
            if password_change_form.is_valid():
                user_password = password_change_form.save()
                update_session_auth_hash(request, user_password)
                messages.success(request, "Your password has been updated sucessfully!")
                return redirect(reverse(profile_namespace))
        elif request.POST.get("action") == "update_phone":
            firebase_user = auth.verify_id_token(request.POST.get("id_token"))
            request.user.customer.phone_number = firebase_user["phone_number"]
            request.user.customer.save()
            return redirect(reverse(profile_namespace))
    return render(
        request,
        "customer/profile.html",
        {
            "form": form,
            "customer_form": customer_form,
            "password_change_form": password_change_form,
        },
    )


@login_required(login_url="/sign-in/?next=/customer/")
def customer_payment(request):
    current_customer = request.user.customer

    if not current_customer.stripe_customer_id:
        customer = stripe.Customer.create()
        current_customer.stripe_customer_id = customer["id"]
        current_customer.save()

    stripe_payment_methods = stripe.PaymentMethod.list(
        customer=current_customer.stripe_customer_id, type="card"
    )

    if stripe_payment_methods and len(stripe_payment_methods.data) > 0:
        payment_method = stripe_payment_methods.data[0]
        current_customer.stripe_payments_method_id = payment_method.id
        current_customer.stripe_card_last_4_digits = payment_method.card.last4
        current_customer.save()
    else:
        current_customer.stripe_payments_method_id = ""
        current_customer.stripe_card_last_4_digits = ""
        current_customer.save()

    if request.method == "POST":
        sp_id = request.user.customer.stripe_payments_method_id
        stripe.PaymentMethod.detach(sp_id)
        current_customer.stripe_payments_method_id = ""
        current_customer.stripe_card_last_4_digits = ""
        current_customer.save()
        return redirect(reverse("customer:payment"))

    if not current_customer.stripe_payments_method_id:
        intent = stripe.SetupIntent.create(
            customer=current_customer.stripe_customer_id,
            payment_method_types=["card"],
        )
        return render(
            request, "customer/payment.html", {"client_secret": intent.client_secret}
        )
    else:
        return render(request, "customer/payment.html")


@login_required(login_url="/sign-in/?next=/customer/")
def customer_create_job(request):
    current_customer = request.user.customer
    current_step = 0

    if not current_customer.stripe_payments_method_id:
        return redirect(reverse("customer:payment"))
    
    has_current_job = Job.objects.filter(
        customer=current_customer,
        status__in=[
            Job.PROCESSING,
            Job.PICKING,
            Job.DELIVERING
        ]
    ).exists()

    if has_current_job:
        messages.warning(request, "You currently have a processing job!")
        return redirect(reverse("customer:current_jobs"))

    created_jobs = Job.objects.filter(
        customer=current_customer, status=Job.CREATING
    ).last()

    job_creation_form = JobCreationForm(instance=created_jobs)
    job_pickup_form = JobPickupForm(instance=created_jobs)
    job_delivery_form = JobDeliveryForm(instance=created_jobs)

    if request.method == "POST":
        if request.POST.get("step") == "1":
            job_creation_form = JobCreationForm(
                request.POST, request.FILES, instance=created_jobs
            )
            if job_creation_form.is_valid():
                created_jobs = job_creation_form.save(commit=False)
                created_jobs.customer = current_customer
                created_jobs.save()
                return redirect(reverse(create_job_namespace))
        elif request.POST.get("step") == "2":
            job_pickup_form = JobPickupForm(request.POST, instance=created_jobs)
            if job_pickup_form.is_valid():
                created_jobs = job_pickup_form.save()
                return redirect(reverse(create_job_namespace))
        elif request.POST.get("step") == "3":
            job_delivery_form = JobDeliveryForm(request.POST, instance=created_jobs)
            if job_delivery_form.is_valid():
                created_jobs = job_delivery_form.save()
                try:
                    url = (
                        "https://maps.googleapis.com/maps/api/distancematrix/json?origins="
                        + created_jobs.pickup_address
                        + "&destinations="
                        + created_jobs.delivery_address
                        + "&mode=transit&key="
                        + settings.DISTANCE_MATRIX_API_KEY
                    )
                    url = url.replace(" ", "")
                    r = requests.get(url, headers={}, data={})

                    distance = r.json()["rows"][0]["elements"][0]["distance"]["value"]
                    duration = r.json()["rows"][0]["elements"][0]["duration"]["value"]

                    print(distance, duration)
                    created_jobs.distance = round(distance / 1000, 2)
                    created_jobs.duration = int(duration / 60)
                    created_jobs.price = created_jobs.distance * 1

                    created_jobs.save()
                except Exception as e:
                    print(e)
                    messages.error(
                        request,
                        "Unfortunately, we do not support delivery for your location!",
                    )
                return redirect(reverse(create_job_namespace))
        elif request.POST.get("step") == "4":
            if created_jobs.price:
                try:
                    payment_intent = stripe.PaymentIntent.create(
                        amount=int(created_jobs.price * 100),
                        currency="usd",
                        customer=current_customer.stripe_customer_id,
                        payment_method=current_customer.stripe_payments_method_id,
                        off_session=True,
                        confirm=True,
                    )
                    Transaction.objects.create(
                        stripe_payment_intent_id=payment_intent["id"],
                        job=created_jobs,
                        amount=created_jobs.price,
                    )
                    created_jobs.status = Job.PROCESSING
                    created_jobs.save()
                    return redirect(reverse("customer:home"))
                except stripe.error.CardError as e:
                    err = e.error
                    # Error code will be authentication_required if authentication is needed
                    print("Code is: %s" % err.code)
                    payment_intent_id = err.payment_intent["id"]
                    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                    messages.error(

                        request,

                        "Oops, something went wrong! Try again!",

                    )

                return redirect(reverse (create_job_namespace))

    if not created_jobs:
        current_step = 1
    elif created_jobs.delivery_name:
        current_step = 4
    elif created_jobs.pickup_name:
        current_step = 3
    else:
        current_step = 2

    return render(
        request,
        "customer/create-job.html",
        {
            "job_creation_form": job_creation_form,
            "job_pickup_form": job_pickup_form,
            "job_delivery_form": job_delivery_form,
            "created_jobs": created_jobs,
            "current_step": current_step,
        },
    )


@login_required(login_url="/sign-in/?next=/customer/")
def customer_current_jobs(request):
    current_customer = request.user.customer
    jobs = Job.objects.filter(
        customer=current_customer,
        status__in=[
            Job.PICKING,
            Job.PROCESSING,
            Job.DELIVERING
        ]
    )
    return render(request, "customer/current-jobs.html", { "jobs": jobs })

@login_required(login_url="/sign-in/?next=/customer/")
def customer_archived_jobs(request):
    current_customer = request.user.customer
    jobs = Job.objects.filter(
        customer=current_customer,
        status__in=[
            Job.COMPLETED,
            Job.CANCELLED
        ]
    )
    return render(request, "customer/archived-jobs.html", { "jobs": jobs })
