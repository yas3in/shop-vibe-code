from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from catalog.models import Product, Category, Brand


def product_list(request):
    products = Product.objects.filter(is_active=True).select_related('price', 'brand', 'category')

    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort', 'newest')

    if category_id:
        try:
            cat = Category.objects.get(pk=category_id)
            products = products.filter(category_id__in=cat.descendant_ids())
        except Category.DoesNotExist:
            pass

    if brand_id:
        products = products.filter(brand_id=brand_id)

    if min_price:
        products = products.filter(price__price__gte=int(min_price))

    if max_price:
        products = products.filter(price__price__lte=int(max_price))

    if sort == 'cheapest':
        products = products.order_by('price__price')
    elif sort == 'expensive':
        products = products.order_by('-price__price')
    elif sort == 'bestselling':
        products = products.order_by('-sold_count')
    elif sort == 'discount':
        products = products.order_by('-price__discount_percent')
    else:
        products = products.order_by('-created_time')

    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    categories = Category.objects.filter(parent__isnull=True)
    brands = Brand.objects.filter(is_active=True)

    return render(request, 'catalog/front/product_list.html', {
        'products': products,
        'categories': categories,
        'brands': brands,
        'current_category': category_id,
        'current_brand': brand_id,
        'current_sort': sort,
        'min_price': min_price or '',
        'max_price': max_price or '',
    })


def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.select_related('price', 'brand', 'category', 'product_type'),
        pk=pk, is_active=True
    )
    images = product.images.all()
    attributes = product.attributes.select_related('product_attribute').all()

    related = Product.objects.filter(
        is_active=True
    ).select_related('price', 'brand', 'category').exclude(pk=product.pk)

    related_by_category = related.filter(category=product.category)[:4]
    related_by_brand = related.filter(brand=product.brand).exclude(
        pk__in=related_by_category.values_list('pk', flat=True)
    )[:4]

    if product.final_price:
        price_range = int(product.final_price * 0.3)
        related_by_price = related.filter(
            price__price__gte=product.final_price - price_range,
            price__price__lte=product.final_price + price_range
        ).exclude(
            pk__in=list(related_by_category.values_list('pk', flat=True)) +
                   list(related_by_brand.values_list('pk', flat=True))
        )[:4]
    else:
        related_by_price = Product.objects.none()

    related_products = list(related_by_category) + list(related_by_brand) + list(related_by_price)
    seen = set()
    unique_related = []
    for p in related_products:
        if p.pk not in seen:
            seen.add(p.pk)
            unique_related.append(p)

    return render(request, 'catalog/front/product_detail.html', {
        'product': product,
        'images': images,
        'attributes': attributes,
        'related_products': unique_related[:8],
    })
