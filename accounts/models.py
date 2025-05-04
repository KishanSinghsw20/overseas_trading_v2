from django.db import models
from django.contrib.auth.models import User


class CompanyLoc(models.Model):
    branch = models.CharField(max_length=20, primary_key=True)
    badd = models.CharField(max_length=255)
    bph = models.CharField(max_length=20)
    baltph = models.CharField(max_length=20, blank=True, null=True)
    bmname = models.CharField(max_length=100)
    bfax = models.CharField(max_length=20, blank=True, null=True)
    bmemail = models.CharField(max_length=100)
    bloc = models.CharField(max_length=100)
    terminus = models.CharField(max_length=100)
    bpassw = models.CharField(max_length=100)
    buname = models.CharField(max_length=100)
    tdet = models.CharField(max_length=255)

    def __str__(self):
        return self.branch

    class Meta:
        verbose_name = "Company Location"
        verbose_name_plural = "Company Locations"


class Client(models.Model):
    cltid = models.CharField(max_length=20, primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="client_profile"
    )
    cname = models.CharField(max_length=100)
    cpass = models.CharField(max_length=100)
    cadd = models.CharField(max_length=255)
    cph = models.CharField(max_length=20)
    cphalt = models.CharField(max_length=20, blank=True, null=True)
    cfax = models.CharField(max_length=20, blank=True, null=True)
    ccperson = models.CharField(max_length=100)
    cdesig = models.CharField(max_length=100)
    cemail = models.CharField(max_length=100)
    cregdt = models.DateField(auto_now_add=True)
    btype = models.CharField(max_length=50)
    profile = models.CharField(max_length=255)

    def __str__(self):
        return self.cname

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class Supplier(models.Model):
    supid = models.CharField(max_length=20, primary_key=True)
    supname = models.CharField(max_length=100)
    supadd = models.CharField(max_length=255)
    sph = models.CharField(max_length=20)
    saltph = models.CharField(max_length=20, blank=True, null=True)
    sfax = models.CharField(max_length=20, blank=True, null=True)
    scper = models.CharField(max_length=100)
    scperdesig = models.CharField(max_length=100)
    compemail = models.CharField(max_length=100)
    suname = models.CharField(max_length=100)
    spass = models.CharField(max_length=100)
    sregdt = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.supname

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"


class Notice(models.Model):
    noticeid = models.AutoField(primary_key=True)
    branch = models.ForeignKey(CompanyLoc, on_delete=models.CASCADE)
    ndt = models.DateField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"Notice {self.noticeid} for {self.branch}"

    class Meta:
        verbose_name = "Notice"
        verbose_name_plural = "Notices"
