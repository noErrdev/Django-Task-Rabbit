from django import forms

from core.models import Courier


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Courier
        fields = ("paypal_email",)
