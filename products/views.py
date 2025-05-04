from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Product, ProdStockMast, BranchStk
from .forms import ProductForm, ProductStockForm, BranchStockForm
from accounts.views import is_admin
import uuid


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})


@login_required
def product_detail(request, prodid):
    product = get_object_or_404(Product, prodid=prodid)
    stock = ProdStockMast.objects.filter(prodid=product).order_by("-stkdt").first()
    branch_stocks = BranchStk.objects.filter(prodid=product)

    return render(
        request,
        "products/product_detail.html",
        {"product": product, "stock": stock, "branch_stocks": branch_stocks},
    )


@login_required
@user_passes_test(is_admin)
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            if not product.prodid:
                product.prodid = f"PRD{uuid.uuid4().hex[:8].upper()}"
            product.save()
            messages.success(request, "Product created successfully!")
            return redirect("product_list")
    else:
        form = ProductForm()

    return render(
        request, "products/product_form.html", {"form": form, "title": "Create Product"}
    )


@login_required
@user_passes_test(is_admin)
def product_update(request, prodid):
    product = get_object_or_404(Product, prodid=prodid)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("product_detail", prodid=product.prodid)
    else:
        form = ProductForm(instance=product)

    return render(
        request, "products/product_form.html", {"form": form, "title": "Update Product"}
    )


@login_required
@user_passes_test(is_admin)
def product_delete(request, prodid):
    product = get_object_or_404(Product, prodid=prodid)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("product_list")

    return render(request, "products/product_confirm_delete.html", {"product": product})


@login_required
@user_passes_test(is_admin)
def stock_create(request, prodid):
    product = get_object_or_404(Product, prodid=prodid)

    if request.method == "POST":
        form = ProductStockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.prodid = product
            stock.save()
            messages.success(request, "Stock updated successfully!")
            return redirect("product_detail", prodid=product.prodid)
    else:
        form = ProductStockForm(initial={"prodid": product})

    return render(
        request, "products/stock_form.html", {"form": form, "product": product}
    )


@login_required
@user_passes_test(is_admin)
def branch_stock_create(request, prodid):
    product = get_object_or_404(Product, prodid=prodid)

    if request.method == "POST":
        form = BranchStockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.prodid = product
            stock.save()
            messages.success(request, "Branch stock updated successfully!")
            return redirect("product_detail", prodid=product.prodid)
    else:
        form = BranchStockForm(initial={"prodid": product})

    return render(
        request, "products/branch_stock_form.html", {"form": form, "product": product}
    )
