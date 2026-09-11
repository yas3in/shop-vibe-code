from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render

from orders.models import Order


@user_passes_test(lambda u: u.is_staff)
def order_list(request):
    orders = Order.objects.select_related("user").order_by("-created_time")
    return render(request, "orders/panel/order_list.html", {"orders": orders})


@user_passes_test(lambda u: u.is_staff)
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items = order.items.select_related("product")
    return render(request, "orders/panel/order_detail.html", {"order": order, "items": items})
