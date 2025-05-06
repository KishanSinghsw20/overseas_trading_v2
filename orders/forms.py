from django import forms
from django.urls import reverse

from products.models import Product
from .models import (
    OrdMast,
    ClientOrd,
    Invoice,
    PayDet,
    ClientOrdDelivery,
    DeliveryTracking,
)


class OrderForm(forms.ModelForm):
    class Meta:
        model = OrdMast
        fields = ["reqdt", "cltid"]
        widgets = {
            "reqdt": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "cltid": forms.Select(attrs={"class": "form-control"}),
        }


class ClientOrderForm(forms.ModelForm):
    class Meta:
        model = ClientOrd
        fields = ["prodid", "quantity"]
        widgets = {
            "prodid": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(
                attrs={"class": "form-control quantity-input", "min": "1"}
            ),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            "invno",
            "ordno",
            "dddt",
            "paydt",
            "gamt",
            "othrchrg1",
            "othrchrg2",
            "othrchrg3",
            "othrchrg4",
            "netamt",
            "recvdt",
            "advpay",
            "rempay",
            "advdt",
            "rempaydt",
        ]
        widgets = {
            "dddt": forms.DateInput(attrs={"type": "date"}),
            "paydt": forms.DateInput(attrs={"type": "date"}),
            "recvdt": forms.DateInput(attrs={"type": "date"}),
            "advdt": forms.DateInput(attrs={"type": "date"}),
            "rempaydt": forms.DateInput(attrs={"type": "date"}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = PayDet
        fields = [
            "invno",
            # "payno",
            "paytype",
            "ddchqno",
            "ddchqdt",
            "on",
            "pstatus",
            "payfor",
        ]
        widgets = {
            "ddchqdt": forms.DateInput(attrs={"type": "date"}),
        }


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = ClientOrdDelivery
        fields = [
            "invno",
            "branch",
            # "delcode",
            "delmode",
            "deldt",
            "delstatus",
            "delcomnts",
            "source",
            "destination",
        ]
        widgets = {
            "deldt": forms.DateInput(attrs={"type": "date"}),
            "delcomnts": forms.Textarea(attrs={"rows": 3}),
        }


class TrackingForm(forms.ModelForm):
    class Meta:
        model = DeliveryTracking
        fields = [
            # "trackingid",
            "delcode",
            "cloc",
            "transno",
            "tmreach",
            "dtreach",
            "tremks",
        ]
        widgets = {
            "dtreach": forms.DateInput(attrs={"type": "date"}),
            "tremks": forms.Textarea(attrs={"rows": 3}),
        }
