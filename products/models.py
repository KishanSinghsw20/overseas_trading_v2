from django.db import models
from accounts.models import CompanyLoc


class Product(models.Model):
    prodid = models.CharField(max_length=20, primary_key=True)
    pname = models.CharField(max_length=100)
    prate = models.DecimalField(max_digits=10, decimal_places=2)
    mfd = models.DateField()
    pdesc = models.TextField()
    madeof = models.CharField(max_length=100)
    wt = models.CharField(max_length=20)
    wtunit = models.CharField(max_length=10)
    minstk = models.IntegerField()
    reorderstk = models.IntegerField()
    pforunit = models.IntegerField()
    img = models.ImageField(upload_to="products/", default="products/default.jpg")
    pcat = models.CharField(max_length=50)

    def __str__(self):
        return self.pname

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProdStockMast(models.Model):
    prodid = models.ForeignKey(Product, on_delete=models.CASCADE)
    stkdt = models.DateField(auto_now_add=True)
    stktype = models.CharField(max_length=50)
    stkqty = models.IntegerField()
    stkunit = models.CharField(max_length=10)
    currstk = models.IntegerField()

    def __str__(self):
        return f"Stock for {self.prodid}"

    class Meta:
        verbose_name = "Product Stock Master"
        verbose_name_plural = "Product Stock Masters"


class BranchStk(models.Model):
    branch = models.ForeignKey(CompanyLoc, on_delete=models.CASCADE)
    prodid = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    dt = models.DateField(auto_now_add=True)
    unit = models.IntegerField()
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"Branch {self.branch} stock for {self.prodid}"

    class Meta:
        verbose_name = "Branch Stock"
        verbose_name_plural = "Branch Stocks"
