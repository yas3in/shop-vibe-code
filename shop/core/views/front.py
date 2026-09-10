from django.shortcuts import render
from catalog.models import Product, Brand


def home(request):
    top_selling = Product.objects.filter(
        is_active=True
    ).select_related('price', 'brand', 'category').order_by('-sold_count')[:8]

    most_discounted = Product.objects.filter(
        is_active=True, price__discount_percent__gt=0
    ).select_related('price', 'brand', 'category').order_by('-price__discount_percent')[:8]

    brands = Brand.objects.filter(is_active=True)

    return render(request, 'core/home.html', {
        'top_selling': top_selling,
        'most_discounted': most_discounted,
        'brands': brands,
    })


def contact(request):
    from catalog.forms import ContactForm
    sent = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sent = True
            form = ContactForm()
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form, 'sent': sent})
