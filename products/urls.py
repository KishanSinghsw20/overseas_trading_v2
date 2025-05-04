from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("create/", views.product_create, name="product_create"),
    path("<str:prodid>/", views.product_detail, name="product_detail"),
    path("<str:prodid>/update/", views.product_update, name="product_update"),
    path("<str:prodid>/delete/", views.product_delete, name="product_delete"),
    path("<str:prodid>/stock/create/", views.stock_create, name="stock_create"),
    path(
        "<str:prodid>/branch-stock/create/",
        views.branch_stock_create,
        name="branch_stock_create",
    ),
]
