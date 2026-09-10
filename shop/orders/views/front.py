import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from catalog.models import Basket, BasketLine, Product
from orders.models import Order, OrderLine, Payment
from addresses.models import Address


@login_required
def basket_view(request):
    basket, _ = Basket.objects.get_or_create(user=request.user, status=Basket.PENDING)
    lines = basket.lines.select_related('product', 'product__price')
    return render(request, 'orders/basket.html', {'basket': basket, 'lines': lines})


@login_required
def basket_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    basket, _ = Basket.objects.get_or_create(user=request.user, status=Basket.PENDING)
    line, created = BasketLine.objects.get_or_create(basket=basket, product=product)
    if not created:
        line.quantity += 1
        line.save()
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('orders:basket')


@login_required
def basket_remove(request, product_id):
    basket = Basket.objects.filter(user=request.user, status=Basket.PENDING).first()
    if basket:
        BasketLine.objects.filter(basket=basket, product_id=product_id).delete()
    return redirect('orders:basket')


@login_required
def basket_update(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        basket = Basket.objects.filter(user=request.user, status=Basket.PENDING).first()
        if basket:
            line = BasketLine.objects.filter(basket=basket, product_id=product_id).first()
            if line:
                if quantity <= 0:
                    line.delete()
                else:
                    line.quantity = quantity
                    line.save()
    return redirect('orders:basket')


@login_required
def checkout_address(request):
    basket = Basket.objects.filter(user=request.user, status=Basket.PENDING).first()
    if not basket or not basket.lines.exists():
        return redirect('orders:basket')
    addresses = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        if address_id:
            address = get_object_or_404(Address, pk=address_id, user=request.user)
            order = Order.objects.create(
                user=request.user,
                address=address,
                total_price=basket.total_price,
            )
            for line in basket.lines.select_related('product', 'product__price'):
                OrderLine.objects.create(
                    order=order,
                    product=line.product,
                    product_title=line.product.title,
                    quantity=line.quantity,
                    price=line.product.price.final_price if hasattr(line.product, 'price') else 0,
                )
            Payment.objects.create(order=order, amount=order.total_price)
            basket.status = Basket.EXPIRED
            basket.save()
            return redirect('orders:payment_gateway', order_id=order.pk)
    return render(request, 'orders/checkout_address.html', {
        'addresses': addresses,
        'basket': basket,
    })


@login_required
def payment_gateway(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user, status=Order.PENDING)
    return render(request, 'orders/payment_gateway.html', {'order': order})


@login_required
def payment_callback(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user, status=Order.PENDING)
    if request.method == 'POST':
        order.status = Order.PAID
        order.save()
        payment = order.payment
        payment.is_paid = True
        payment.paid_time = timezone.now()
        payment.transaction_id = str(uuid.uuid4())[:20]
        payment.save()
        for line in order.lines.all():
            if line.product:
                line.product.sold_count += line.quantity
                line.product.stock = max(0, line.product.stock - line.quantity)
                line.product.save()
        return redirect('orders:order_detail', pk=order.pk)
    return redirect('orders:payment_gateway', order_id=order.pk)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    lines = order.lines.all()
    return render(request, 'orders/order_detail.html', {'order': order, 'lines': lines})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_time')
    return render(request, 'orders/order_list.html', {'orders': orders})
