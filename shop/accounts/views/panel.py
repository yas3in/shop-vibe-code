from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from orders.models import Order


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "accounts/panel/profile.html", {"orders": orders})
