from django.urls import path
from . import views

urlpatterns = [
    path("", views.order_list, name="order_list"),
    path("create/", views.order_create, name="order_create"),
    path("<str:ordno>/", views.order_detail, name="order_detail"),
    path("<str:ordno>/add-item/", views.order_add_item, name="order_add_item"),
    path(
        "<str:ordno>/generate-invoice/", views.generate_invoice, name="generate_invoice"
    ),
    path("invoices/<str:invno>/", views.invoice_detail, name="invoice_detail"),
    path("invoices/<str:invno>/payment/", views.add_payment, name="add_payment"),
    path("invoices/<str:invno>/delivery/", views.add_delivery, name="add_delivery"),
    path(
        "delivery/<str:delcode>/tracking/",
        views.delivery_tracking,
        name="delivery_tracking",
    ),
    path(
        "delivery/<str:delcode>/tracking/add/", views.add_tracking, name="add_tracking"
    ),
]
