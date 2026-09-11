from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from addresses.models import Address
from catalog.models import Basket, BasketLine, Product
from orders.forms import FakePaymentForm
from orders.models import Order, OrderItem, Payment


def get_active_basket(user):
    basket, _ = Basket.objects.get_or_create(user=user, status="pending")
    return basket


@login_required
def basket_view(request):
    basket = get_active_basket(request.user)
    lines = basket.lines.select_related("product", "product__price")
    return render(request, "orders/basket.html", {"basket": basket, "lines": lines})


@login_required
def basket_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    basket = get_active_basket(request.user)
    line, created = BasketLine.objects.get_or_create(basket=basket, product=product)
    if not created and line.quantity < product.stock:
        line.quantity += 1
        line.save()
    next_url = request.GET.get("next")
    if next_url:
        return redirect(next_url)
    return redirect("basket")


@login_required
def basket_remove(request, product_id):
    basket = Basket.objects.filter(user=request.user, status="pending").first()
    if basket:
        BasketLine.objects.filter(basket=basket, product_id=product_id).delete()
    return redirect("basket")


@login_required
def basket_update(request, product_id):
    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 1))
        except (TypeError, ValueError):
            quantity = 1
        basket = Basket.objects.filter(user=request.user, status="pending").first()
        if basket:
            line = BasketLine.objects.filter(basket=basket, product_id=product_id).first()
            if line:
                if quantity <= 0:
                    line.delete()
                elif quantity <= line.product.stock:
                    line.quantity = quantity
                    line.save()
    return redirect("basket")


@login_required
def checkout_address(request):
    basket = Basket.objects.filter(user=request.user, status="pending").first()
    if not basket or not basket.lines.exists():
        return redirect("basket")
    addresses = Address.objects.filter(user=request.user)
    default_address = addresses.filter(is_default=True).first()
    if request.method == "POST":
        address_id = request.POST.get("address_id")
        if address_id:
            address = get_object_or_404(Address, pk=address_id, user=request.user)
            order = Order.objects.create(
                user=request.user,
                receipt_name=address.receipt_name,
                phone_number=address.phone_number,
                city=address.city,
                postal_code=address.postal_code,
                full_address=address.full_address,
                address_detail=address.address_detail,
                total_price=basket.total_price,
            )
            for line in basket.lines.select_related("product", "product__price"):
                OrderItem.objects.create(
                    order=order,
                    product=line.product,
                    product_title=line.product.title,
                    unit_price=line.product.final_price or line.product.price.price,
                    quantity=line.quantity,
                )
            Payment.objects.create(order=order, amount=order.total_price)
            basket.status = "expired"
            basket.save()
            return redirect("payment_gateway", order_id=order.pk)
        else:
            return redirect("addresses:address_create")
    return render(request, "orders/checkout_address.html", {
        "addresses": addresses,
        "default_address": default_address,
        "basket": basket,
    })


@login_required
def payment_gateway(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user, status="pending")
    if request.method == "POST":
        form = FakePaymentForm(request.POST)
        if form.is_valid():
            return redirect("payment_callback", order_id=order.pk)
    else:
        form = FakePaymentForm()
    return render(request, "orders/payment_gateway.html", {"order": order, "form": form})


@login_required
def payment_callback(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    payment = order.payments.order_by("-created_time").first()
    if order.status == "pending" and request.method == "POST":
        order.status = "paid"
        order.save()
        if payment:
            payment.status = "success"
            payment.save()
        for item in order.items.select_related("product"):
            if item.product:
                item.product.sold_count += item.quantity
                item.product.stock = max(0, item.product.stock - item.quantity)
                item.product.save()
        return redirect("order_detail", pk=order.pk)
    return redirect("payment_gateway", order_id=order.pk)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    items = order.items.select_related("product")
    return render(request, "orders/order_detail.html", {"order": order, "items": items})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_time")
    return render(request, "orders/order_list.html", {"orders": orders})
