from django import forms
from .models import Product, ProdStockMast, BranchStk


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "prodid",
            "pname",
            "prate",
            "mfd",
            "pdesc",
            "madeof",
            "wt",
            "wtunit",
            "minstk",
            "reorderstk",
            "pforunit",
            "img",
            "pcat",
        ]
        widgets = {
            "mfd": forms.DateInput(attrs={"type": "date"}),
            "pdesc": forms.Textarea(attrs={"rows": 3}),
        }


class ProductStockForm(forms.ModelForm):
    class Meta:
        model = ProdStockMast
        fields = ["stktype", "stkqty", "stkunit", "currstk"]  # "prodid",


class BranchStockForm(forms.ModelForm):
    class Meta:
        model = BranchStk
        fields = ["branch", "qty", "unit", "type"]  # "prodid",
