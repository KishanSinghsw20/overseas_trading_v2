from django.db import models
from accounts.models import Client, CompanyLoc, Supplier
from products.models import Product


class OrdMast(models.Model):
    ordno = models.CharField(max_length=20, primary_key=True)
    ordt = models.DateField(auto_now_add=True)
    reqdt = models.DateField()
    totamt = models.DecimalField(max_digits=12, decimal_places=2)
    cltid = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.ordno}"

    class Meta:
        verbose_name = "Order Master"
        verbose_name_plural = "Order Masters"


class ClientOrd(models.Model):
    ordno = models.ForeignKey(OrdMast, on_delete=models.CASCADE)
    prodid = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    amt = models.DecimalField(max_digits=12, decimal_places=2)
    qtygv = models.IntegerField()

    def __str__(self):
        return f"Client order for {self.ordno}"

    class Meta:
        verbose_name = "Client Order"
        verbose_name_plural = "Client Orders"


class Invoice(models.Model):
    invno = models.CharField(max_length=20, primary_key=True)
    ordno = models.ForeignKey(OrdMast, on_delete=models.CASCADE)
    dddt = models.DateField()
    paydt = models.DateField()
    gamt = models.DecimalField(max_digits=12, decimal_places=2)
    othrchrg1 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    othrchrg2 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    othrchrg3 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    othrchrg4 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    netamt = models.DecimalField(max_digits=12, decimal_places=2)
    recvdt = models.DateField()
    advpay = models.DecimalField(max_digits=12, decimal_places=2)
    rempay = models.DecimalField(max_digits=12, decimal_places=2)
    advdt = models.DateField()
    rempaydt = models.DateField()

    def __str__(self):
        return f"Invoice {self.invno}"

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"


class PayDet(models.Model):
    invno = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payno = models.CharField(max_length=20, primary_key=True)
    paytype = models.CharField(max_length=50)
    ddchqno = models.CharField(max_length=50, blank=True, null=True)
    ddchqdt = models.DateField(blank=True, null=True)
    on = models.CharField(max_length=100, blank=True, null=True)
    pstatus = models.CharField(max_length=50)
    payfor = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment {self.payno} for {self.invno}"

    class Meta:
        verbose_name = "Payment Detail"
        verbose_name_plural = "Payment Details"


class ClientOrdDelivery(models.Model):
    invno = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    branch = models.ForeignKey(CompanyLoc, on_delete=models.CASCADE)
    delcode = models.CharField(max_length=20, primary_key=True)
    delmode = models.CharField(max_length=50)
    deldt = models.DateField()
    delstatus = models.CharField(max_length=50)
    delcomnts = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return f"Delivery {self.delcode} for {self.invno}"

    class Meta:
        verbose_name = "Client Order Delivery"
        verbose_name_plural = "Client Order Deliveries"


class DeliveryTracking(models.Model):
    trackingid = models.CharField(max_length=20, primary_key=True)
    cloc = models.CharField(max_length=100)
    transno = models.CharField(max_length=50)
    delcode = models.ForeignKey(ClientOrdDelivery, on_delete=models.CASCADE)
    tmreach = models.IntegerField()
    dtreach = models.DateField()
    tremks = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Tracking {self.trackingid} for {self.delcode}"

    class Meta:
        verbose_name = "Delivery Tracking"
        verbose_name_plural = "Delivery Trackings"


class TenderMast(models.Model):
    tendid = models.CharField(max_length=20, primary_key=True)
    supid = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    tcalldt = models.DateField()
    branch = models.ForeignKey(CompanyLoc, on_delete=models.CASCADE)
    supname = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Tender {self.tendid} from {self.supname}"

    class Meta:
        verbose_name = "Tender Master"
        verbose_name_plural = "Tender Masters"


class TenderIni(models.Model):
    prodid = models.ForeignKey(Product, on_delete=models.CASCADE)
    branch = models.ForeignKey(CompanyLoc, on_delete=models.CASCADE)
    budgetp = models.CharField(max_length=20)
    dmaker = models.CharField(max_length=100)
    forunits = models.CharField(max_length=20)
    measin = models.CharField(max_length=10)

    def __str__(self):
        return f"Tender initialization for {self.prodid}"

    class Meta:
        verbose_name = "Tender Initialization"
        verbose_name_plural = "Tender Initializations"


class TenderDet(models.Model):
    tendid = models.ForeignKey(TenderMast, on_delete=models.CASCADE)
    prodid = models.ForeignKey(Product, on_delete=models.CASCADE)
    qprice = models.DecimalField(max_digits=12, decimal_places=2)
    forunits = models.CharField(max_length=20)
    measin = models.CharField(max_length=10)

    def __str__(self):
        return f"Tender details for {self.tendid}"

    class Meta:
        verbose_name = "Tender Detail"
        verbose_name_plural = "Tender Details"


class PurchaseMast(models.Model):
    purid = models.CharField(max_length=20, primary_key=True)
    branch = models.ForeignKey(CompanyLoc, on_delete=models.CASCADE)
    supid = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    sorddt = models.DateField()
    srecvdt = models.DateField()

    def __str__(self):
        return f"Purchase {self.purid}"

    class Meta:
        verbose_name = "Purchase Master"
        verbose_name_plural = "Purchase Masters"


class BranchPurchase(models.Model):
    purid = models.ForeignKey(PurchaseMast, on_delete=models.CASCADE)
    prodid = models.ForeignKey(Product, on_delete=models.CASCADE)
    pqty = models.IntegerField()
    pamt = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Branch purchase for {self.purid}"

    class Meta:
        verbose_name = "Branch Purchase"
        verbose_name_plural = "Branch Purchases"


class SalesReturn(models.Model):
    invno = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    prodid = models.ForeignKey(Product, on_delete=models.CASCADE)
    qtyr = models.IntegerField()
    rem = models.CharField(max_length=255, blank=True, null=True)
    retdt = models.DateField()

    def __str__(self):
        return f"Sales return for {self.invno}"

    class Meta:
        verbose_name = "Sales Return"
        verbose_name_plural = "Sales Returns"
