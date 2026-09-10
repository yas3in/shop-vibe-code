from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from catalog.models import Product, ProductPrice, ProductImage
from catalog.forms import ProductForm, ProductPriceForm, ProductImageForm


@login_required
def dashboard(request):
    products = Product.objects.select_related('price', 'brand', 'category').order_by('-created_time')[:10]
    return render(request, 'catalog/panel/dashboard.html', {'products': products})


@login_required
def panel_product_list(request):
    products = Product.objects.select_related('price', 'brand', 'category').order_by('-created_time')
    return render(request, 'catalog/panel/product_list.html', {'products': products})


@login_required
def panel_product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        price_form = ProductPriceForm(request.POST)
        if form.is_valid() and price_form.is_valid():
            product = form.save()
            price = price_form.save(commit=False)
            price.product = product
            price.save()
            images = request.FILES.getlist('gallery')
            for img in images:
                ProductImage.objects.create(product=product, image=img)
            return redirect('catalog:panel_product_list')
    else:
        form = ProductForm()
        price_form = ProductPriceForm()
    return render(request, 'catalog/panel/product_form.html', {
        'form': form,
        'price_form': price_form,
        'editing': False,
    })


@login_required
def panel_product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    price_obj = getattr(product, 'price', None)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        price_form = ProductPriceForm(request.POST, instance=price_obj)
        if form.is_valid() and price_form.is_valid():
            product = form.save()
            price = price_form.save(commit=False)
            price.product = product
            price.save()
            images = request.FILES.getlist('gallery')
            for img in images:
                ProductImage.objects.create(product=product, image=img)
            return redirect('catalog:panel_product_list')
    else:
        form = ProductForm(instance=product)
        price_form = ProductPriceForm(instance=price_obj)
    return render(request, 'catalog/panel/product_form.html', {
        'form': form,
        'price_form': price_form,
        'product': product,
        'editing': True,
    })


@login_required
def panel_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('catalog:panel_product_list')
    return render(request, 'catalog/panel/product_confirm_delete.html', {'product': product})

