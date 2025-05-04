from django.contrib import admin
from .models import (
    OrdMast,
    ClientOrd,
    Invoice,
    PayDet,
    ClientOrdDelivery,
    DeliveryTracking,
    TenderMast,
    TenderIni,
    TenderDet,
    PurchaseMast,
    BranchPurchase,
    SalesReturn,
)


class ClientOrdInline(admin.TabularInline):
    model = ClientOrd
    extra = 1


@admin.register(OrdMast)
class OrdMastAdmin(admin.ModelAdmin):
    list_display = ("ordno", "cltid", "ordt", "reqdt", "totamt")
    search_fields = ("ordno", "cltid__cname")
    list_filter = ("ordt", "reqdt")
    inlines = [ClientOrdInline]


@admin.register(ClientOrd)
class ClientOrdAdmin(admin.ModelAdmin):
    list_display = ("ordno", "prodid", "quantity", "rate", "amt")
    list_filter = ("ordno",)


class PayDetInline(admin.TabularInline):
    model = PayDet
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invno", "ordno", "recvdt", "paydt", "netamt", "rempay")
    search_fields = ("invno", "ordno__ordno")
    list_filter = ("recvdt", "paydt")
    inlines = [PayDetInline]


@admin.register(PayDet)
class PayDetAdmin(admin.ModelAdmin):
    list_display = ("payno", "invno", "paytype", "ddchqdt", "pstatus")
    list_filter = ("paytype", "pstatus", "ddchqdt")


@admin.register(ClientOrdDelivery)
class ClientOrdDeliveryAdmin(admin.ModelAdmin):
    list_display = ("delcode", "invno", "branch", "delmode", "deldt", "delstatus")
    search_fields = ("delcode", "invno__invno")
    list_filter = ("branch", "delmode", "delstatus", "deldt")


@admin.register(DeliveryTracking)
class DeliveryTrackingAdmin(admin.ModelAdmin):
    list_display = ("trackingid", "delcode", "cloc", "dtreach", "tmreach")
    search_fields = ("trackingid", "delcode__delcode", "cloc")
    list_filter = ("dtreach",)


@admin.register(TenderMast)
class TenderMastAdmin(admin.ModelAdmin):
    list_display = ("tendid", "supid", "branch", "tcalldt", "status")
    search_fields = ("tendid", "supname")
    list_filter = ("branch", "status", "tcalldt")


@admin.register(TenderIni)
class TenderIniAdmin(admin.ModelAdmin):
    list_display = ("prodid", "branch", "budgetp", "dmaker")
    list_filter = ("branch",)


@admin.register(TenderDet)
class TenderDetAdmin(admin.ModelAdmin):
    list_display = ("tendid", "prodid", "qprice", "forunits")
    list_filter = ("tendid",)


@admin.register(PurchaseMast)
class PurchaseMastAdmin(admin.ModelAdmin):
    list_display = ("purid", "branch", "supid", "sorddt", "srecvdt")
    search_fields = ("purid",)
    list_filter = ("branch", "sorddt", "srecvdt")


@admin.register(BranchPurchase)
class BranchPurchaseAdmin(admin.ModelAdmin):
    list_display = ("purid", "prodid", "pqty", "pamt")
    list_filter = ("purid",)


@admin.register(SalesReturn)
class SalesReturnAdmin(admin.ModelAdmin):
    list_display = ("invno", "prodid", "qtyr", "retdt")
    search_fields = ("invno__invno",)
    list_filter = ("retdt",)
