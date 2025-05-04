from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client, CompanyLoc, Supplier


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ClientRegisterForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "cname",
            "cadd",
            "cph",
            "cphalt",
            "cfax",
            "ccperson",
            "cdesig",
            "btype",
            "profile",
        ]
        widgets = {
            "cadd": forms.Textarea(attrs={"rows": 3}),
            "profile": forms.Textarea(attrs={"rows": 3}),
        }


class CompanyLocForm(forms.ModelForm):
    class Meta:
        model = CompanyLoc
        fields = [
            "branch",
            "badd",
            "bph",
            "baltph",
            "bmname",
            "bfax",
            "bmemail",
            "bloc",
            "terminus",
            "buname",
            "bpassw",
            "tdet",
        ]
        widgets = {
            "badd": forms.Textarea(attrs={"rows": 3}),
            "tdet": forms.Textarea(attrs={"rows": 3}),
            "bpassw": forms.PasswordInput(),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            "supid",
            "supname",
            "supadd",
            "sph",
            "saltph",
            "sfax",
            "scper",
            "scperdesig",
            "compemail",
            "suname",
            "spass",
        ]
        widgets = {
            "supadd": forms.Textarea(attrs={"rows": 3}),
            "spass": forms.PasswordInput(),
        }
