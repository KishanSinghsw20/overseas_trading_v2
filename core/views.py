from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Product
from orders.models import OrdMast
from accounts.models import Client


def home(request):
    products = Product.objects.all().order_by("-mfd")[:6]
    return render(request, "core/home.html", {"products": products})


@login_required
def dashboard(request):
    if hasattr(request.user, "client_profile"):
        # Client dashboard
        client = request.user.client_profile
        orders = OrdMast.objects.filter(cltid=client).order_by("-ordt")[:5]
        return render(
            request, "core/client_dashboard.html", {"client": client, "orders": orders}
        )
    else:
        # Admin dashboard
        products_count = Product.objects.count()
        clients_count = Client.objects.count()
        orders_count = OrdMast.objects.count()
        recent_orders = OrdMast.objects.all().order_by("-ordt")[:5]
        return render(
            request,
            "core/admin_dashboard.html",
            {
                "products_count": products_count,
                "clients_count": clients_count,
                "orders_count": orders_count,
                "recent_orders": recent_orders,
            },
        )
