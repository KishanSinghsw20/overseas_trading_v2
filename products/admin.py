from django.contrib import admin
from .models import Product, ProdStockMast, BranchStk


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("prodid", "pname", "prate", "pcat", "mfd")
    search_fields = ("prodid", "pname", "pdesc")
    list_filter = ("pcat", "mfd")


@admin.register(ProdStockMast)
class ProdStockMastAdmin(admin.ModelAdmin):
    list_display = ("prodid", "stkdt", "stktype", "stkqty", "currstk")
    list_filter = ("stkdt", "stktype")


@admin.register(BranchStk)
class BranchStkAdmin(admin.ModelAdmin):
    list_display = ("branch", "prodid", "qty", "dt", "type")
    list_filter = ("branch", "dt", "type")
