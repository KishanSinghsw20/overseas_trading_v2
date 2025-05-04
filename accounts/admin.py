from django.contrib import admin
from .models import CompanyLoc, Client, Supplier, Notice


@admin.register(CompanyLoc)
class CompanyLocAdmin(admin.ModelAdmin):
    list_display = ("branch", "bloc", "bmname", "bph", "bmemail")
    search_fields = ("branch", "bloc", "bmname")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("cltid", "cname", "ccperson", "cph", "cemail", "cregdt")
    search_fields = ("cltid", "cname", "ccperson", "cemail")
    list_filter = ("cregdt", "btype")


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("supid", "supname", "scper", "sph", "compemail", "sregdt")
    search_fields = ("supid", "supname", "scper", "compemail")
    list_filter = ("sregdt",)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("noticeid", "branch", "ndt", "content")
    list_filter = ("branch", "ndt")
