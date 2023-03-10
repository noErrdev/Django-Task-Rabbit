import random
import string
from django.contrib import admin, messages
from django.conf import settings
from paypalrestsdk import configure, Payout
from .models import Customer, Courier, Category, Job, Transaction


configure(
    {
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_APP_SECRET_KEY,
    }
)


admin.site.register(Customer)
admin.site.register(Job)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ["full_name", "paypal_email", "balance"]
    actions = ["payment_to_courier"]

    @admin.action(description="Payment to couriers")
    def payment_to_courier(self, request, queryset):
        payout_items = []
        transaction_querysets = []

        for courier in queryset:
            if courier.paypal_email:
                courier_in_transactions = Transaction.objects.filter(
                    job__courier=courier, status=Transaction.CASH_IN
                )
                if courier_in_transactions:
                    transaction_querysets.append(courier_in_transactions)
                    total_amount = sum(t.amount for t in courier_in_transactions)
                    balance = round(total_amount * 0.7, 2)
                    payout_items.append(
                        {
                            "recipient_type": "EMAIL",
                            "amount": {"value": balance, "currency": "USD"},
                            "receiver": courier.paypal_email,
                            "note": "Thank you.",
                            "sender_item_id": str(courier.id),
                        }
                    )
        sender_batch_id = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
        payout = Payout({
            "sender_batch_header": {
                "sender_batch_id": sender_batch_id,
                "email_subject": "You have a payment"
            },
            "items": payout_items,
        })

        try:
            if payout.create():
                for t in transaction_querysets:
                    t.update(status=Transaction.CASH_OUT)
                messages.success(request, "Payout-%s created successfully!" % (payout.batch_header.payout_batch_id))
        except Exception as e:
                messages.error(request, str(e))

    def full_name(self, obj):
        return obj.user.get_full_name()

    def balance(self, obj):
        transactions = Transaction.objects.filter(
            job__courier=obj, status=Transaction.CASH_IN
        )
        total_amount = sum(t.amount for t in transactions)
        balance = round(total_amount * 0.7, 2)
        return balance


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "stripe_payment_intent_id",
        "customer",
        "courier",
        "courier_paypal_email",
        "job",
        "amount",
        "status",
        "created_at",
    ]
    list_filter = ("status",)

    def customer(self, obj):
        return obj.job.customer

    def courier(self, obj):
        return obj.job.courier

    def courier_paypal_email(self, obj):
        return obj.job.courier.paypal_email if obj.job.courier else None
