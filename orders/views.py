from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from .models import (
    OrdMast,
    ClientOrd,
    Invoice,
    PayDet,
    ClientOrdDelivery,
    DeliveryTracking,
)
from .forms import (
    OrderForm,
    ClientOrderForm,
    InvoiceForm,
    PaymentForm,
    DeliveryForm,
    TrackingForm,
)
from accounts.models import Client
from products.models import Product
from accounts.views import is_admin
import uuid
from datetime import datetime, timedelta


@login_required
def order_list(request):
    if hasattr(request.user, "client_profile"):
        client = request.user.client_profile
        orders = OrdMast.objects.filter(cltid=client).order_by("-ordt")
    else:
        orders = OrdMast.objects.all().order_by("-ordt")

    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
def order_detail(request, ordno):
    order = get_object_or_404(OrdMast, ordno=ordno)

    # Check if user has permission to view this order
    if hasattr(request.user, "client_profile"):
        client = request.user.client_profile
        if order.cltid != client:
            messages.error(request, "You do not have permission to view this order.")
            return redirect("order_list")

    order_items = ClientOrd.objects.filter(ordno=order)

    try:
        invoice = Invoice.objects.get(ordno=order)
        payments = PayDet.objects.filter(invno=invoice)
        deliveries = ClientOrdDelivery.objects.filter(invno=invoice)
    except Invoice.DoesNotExist:
        invoice = None
        payments = None
        deliveries = None

    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order,
            "order_items": order_items,
            "invoice": invoice,
            "payments": payments,
            "deliveries": deliveries,
        },
    )


@login_required
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.ordno = f"ORD{uuid.uuid4().hex[:8].upper()}"

                if hasattr(request.user, "client_profile"):
                    client = request.user.client_profile
                    order.cltid = client

                order.totamt = 0  # Will be updated as items are added
                order.save()

                messages.success(
                    request, "Order created successfully! Now add items to your order."
                )
                return redirect("order_add_item", ordno=order.ordno)
    else:
        form = OrderForm()

        if hasattr(request.user, "client_profile"):
            client = request.user.client_profile
            form.fields["cltid"].initial = client
            form.fields["cltid"].widget.attrs["readonly"] = True

    return render(
        request, "orders/order_form.html", {"form": form, "title": "Create Order"}
    )


@login_required
def order_add_item(request, ordno):
    order = get_object_or_404(OrdMast, ordno=ordno)

    # Check if user has permission to modify this order
    if hasattr(request.user, "client_profile"):
        client = request.user.client_profile
        if order.cltid != client:
            messages.error(request, "You do not have permission to modify this order.")
            return redirect("order_list")

    if request.method == "POST":
        form = ClientOrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                item = form.save(commit=False)
                item.ordno = order

                # Calculate amount
                product = item.prodid
                item.rate = product.prate
                item.amt = item.quantity * item.rate
                item.qtygv = (
                    item.quantity
                )  # Initially, we plan to give the full quantity

                item.save()

                # Update order total
                order.totamt += item.amt
                order.save()

                messages.success(request, "Item added to order successfully!")

                if "add_another" in request.POST:
                    return redirect("order_add_item", ordno=order.ordno)
                else:
                    return redirect("order_detail", ordno=order.ordno)
    else:
        form = ClientOrderForm()

    existing_items = ClientOrd.objects.filter(ordno=order)

    return render(
        request,
        "orders/order_item_form.html",
        {"form": form, "order": order, "existing_items": existing_items},
    )


@login_required
@user_passes_test(is_admin)
def generate_invoice(request, ordno):
    order = get_object_or_404(OrdMast, ordno=ordno)

    try:
        # Check if invoice already exists
        invoice = Invoice.objects.get(ordno=order)
        messages.warning(request, "Invoice already exists for this order.")
        return redirect("order_detail", ordno=ordno)
    except Invoice.DoesNotExist:
        # Generate new invoice
        invoice = Invoice()
        invoice.invno = f"INV{uuid.uuid4().hex[:8].upper()}"
        invoice.ordno = order
        invoice.dddt = datetime.now().date() + timedelta(
            days=7
        )  # Expected delivery in 7 days
        invoice.paydt = datetime.now().date() + timedelta(
            days=30
        )  # Payment due in 30 days
        invoice.gamt = order.totamt
        invoice.netamt = order.totamt  # Can be modified to include taxes, etc.
        invoice.recvdt = datetime.now().date()
        invoice.advpay = 0
        invoice.rempay = invoice.netamt
        invoice.advdt = datetime.now().date()
        invoice.rempaydt = invoice.paydt
        invoice.save()

        messages.success(request, "Invoice generated successfully!")
        return redirect("invoice_detail", invno=invoice.invno)


@login_required
def invoice_detail(request, invno):
    invoice = get_object_or_404(Invoice, invno=invno)

    # Check if user has permission to view this invoice
    if hasattr(request.user, "client_profile"):
        client = request.user.client_profile
        if invoice.ordno.cltid != client:
            messages.error(request, "You do not have permission to view this invoice.")
            return redirect("order_list")

    order_items = ClientOrd.objects.filter(ordno=invoice.ordno)
    payments = PayDet.objects.filter(invno=invoice)
    deliveries = ClientOrdDelivery.objects.filter(invno=invoice)

    return render(
        request,
        "orders/invoice_detail.html",
        {
            "invoice": invoice,
            "order_items": order_items,
            "payments": payments,
            "deliveries": deliveries,
        },
    )


@login_required
@user_passes_test(is_admin)
def add_payment(request, invno):
    invoice = get_object_or_404(Invoice, invno=invno)

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                payment = form.save(commit=False)
                payment.invno = invoice
                payment.payno = f"PAY{uuid.uuid4().hex[:8].upper()}"
                payment.save()

                # Update invoice payment status
                if payment.payfor == "Advance":
                    invoice.advpay += float(request.POST.get("amount", 0))
                    invoice.rempay = invoice.netamt - invoice.advpay
                else:
                    amount = float(request.POST.get("amount", 0))
                    if amount > invoice.rempay:
                        amount = invoice.rempay
                    invoice.rempay -= amount

                invoice.save()

                messages.success(request, "Payment recorded successfully!")
                return redirect("invoice_detail", invno=invoice.invno)
    else:
        form = PaymentForm(initial={"invno": invoice})

    return render(
        request, "orders/payment_form.html", {"form": form, "invoice": invoice}
    )


@login_required
@user_passes_test(is_admin)
def add_delivery(request, invno):
    invoice = get_object_or_404(Invoice, invno=invno)

    if request.method == "POST":
        form = DeliveryForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.invno = invoice
            delivery.delcode = f"DEL{uuid.uuid4().hex[:8].upper()}"
            delivery.save()

            messages.success(request, "Delivery information added successfully!")
            return redirect("invoice_detail", invno=invoice.invno)
    else:
        form = DeliveryForm(initial={"invno": invoice})

    return render(
        request, "orders/delivery_form.html", {"form": form, "invoice": invoice}
    )


@login_required
def delivery_tracking(request, delcode):
    delivery = get_object_or_404(ClientOrdDelivery, delcode=delcode)

    # Check if user has permission to view this delivery
    if hasattr(request.user, "client_profile"):
        client = request.user.client_profile
        if delivery.invno.ordno.cltid != client:
            messages.error(
                request, "You do not have permission to view this delivery tracking."
            )
            return redirect("order_list")

    tracking_points = DeliveryTracking.objects.filter(delcode=delivery).order_by(
        "dtreach", "tmreach"
    )

    return render(
        request,
        "orders/delivery_tracking.html",
        {"delivery": delivery, "tracking_points": tracking_points},
    )


@login_required
@user_passes_test(is_admin)
def add_tracking(request, delcode):
    delivery = get_object_or_404(ClientOrdDelivery, delcode=delcode)

    if request.method == "POST":
        form = TrackingForm(request.POST)
        if form.is_valid():
            tracking = form.save(commit=False)
            tracking.delcode = delivery
            tracking.trackingid = f"TRK{uuid.uuid4().hex[:8].upper()}"
            tracking.save()

            # Update delivery status if needed
            if delivery.delstatus != "Delivered":
                delivery.delstatus = "In Transit"
                delivery.save()

            messages.success(request, "Tracking information added successfully!")
            return redirect("delivery_tracking", delcode=delivery.delcode)
    else:
        form = TrackingForm(initial={"delcode": delivery})

    return render(
        request, "orders/tracking_form.html", {"form": form, "delivery": delivery}
    )
