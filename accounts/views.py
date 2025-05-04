from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import UserRegisterForm, ClientRegisterForm, CompanyLocForm, SupplierForm
from .models import Client, CompanyLoc, Supplier
import uuid


def is_admin(user):
    return not hasattr(user, "client_profile")


def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        client_form = ClientRegisterForm(request.POST)

        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()

            client = client_form.save(commit=False)
            client.user = user
            client.cltid = f"CLT{uuid.uuid4().hex[:8].upper()}"
            client.cpass = user.password  # Not secure, but matches the requirement
            client.cemail = user.email
            client.save()

            messages.success(
                request, f"Account created for {user.username}! You can now log in."
            )
            return redirect("login")
    else:
        user_form = UserRegisterForm()
        client_form = ClientRegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"user_form": user_form, "client_form": client_form},
    )


@login_required
def profile(request):
    if hasattr(request.user, "client_profile"):
        client = request.user.client_profile
        return render(request, "accounts/client_profile.html", {"client": client})
    else:
        return render(request, "accounts/admin_profile.html")


@login_required
@user_passes_test(is_admin)
def client_list(request):
    clients = Client.objects.all()
    return render(request, "accounts/client_list.html", {"clients": clients})


@login_required
@user_passes_test(is_admin)
def client_detail(request, cltid):
    client = get_object_or_404(Client, cltid=cltid)
    return render(request, "accounts/client_detail.html", {"client": client})


@login_required
@user_passes_test(is_admin)
def branch_list(request):
    branches = CompanyLoc.objects.all()
    return render(request, "accounts/branch_list.html", {"branches": branches})


@login_required
@user_passes_test(is_admin)
def branch_create(request):
    if request.method == "POST":
        form = CompanyLocForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Branch created successfully!")
            return redirect("branch_list")
    else:
        form = CompanyLocForm()

    return render(
        request, "accounts/branch_form.html", {"form": form, "title": "Create Branch"}
    )


@login_required
@user_passes_test(is_admin)
def branch_update(request, branch):
    branch_obj = get_object_or_404(CompanyLoc, branch=branch)

    if request.method == "POST":
        form = CompanyLocForm(request.POST, instance=branch_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Branch updated successfully!")
            return redirect("branch_list")
    else:
        form = CompanyLocForm(instance=branch_obj)

    return render(
        request, "accounts/branch_form.html", {"form": form, "title": "Update Branch"}
    )


@login_required
@user_passes_test(is_admin)
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, "accounts/supplier_list.html", {"suppliers": suppliers})


@login_required
@user_passes_test(is_admin)
def supplier_create(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.supid = f"SUP{uuid.uuid4().hex[:8].upper()}"
            supplier.save()
            messages.success(request, "Supplier created successfully!")
            return redirect("supplier_list")
    else:
        form = SupplierForm()

    return render(
        request,
        "accounts/supplier_form.html",
        {"form": form, "title": "Create Supplier"},
    )
