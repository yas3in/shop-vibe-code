from catalog.models import Category, Brand, Basket


def store(request):
    categories = Category.objects.filter(parent__isnull=True)
    brands = Brand.objects.filter(is_active=True)
    basket_count = 0
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user, status=Basket.PENDING).first()
        if basket:
            basket_count = basket.total_items
    return {
        'all_categories': categories,
        'all_brands': brands,
        'basket_count': basket_count,
    }
