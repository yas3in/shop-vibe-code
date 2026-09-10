from django.urls import path
from orders.views import front

app_name = 'orders'

urlpatterns = [
    path('basket/', front.basket_view, name='basket'),
    path('basket/add/<int:product_id>/', front.basket_add, name='basket_add'),
    path('basket/remove/<int:product_id>/', front.basket_remove, name='basket_remove'),
    path('basket/update/<int:product_id>/', front.basket_update, name='basket_update'),
    path('checkout/', front.checkout_address, name='checkout_address'),
    path('my-orders/', front.order_list, name='order_list'),
    path('order/<int:pk>/', front.order_detail, name='order_detail'),
    path('payment/gateway/<int:order_id>/', front.payment_gateway, name='payment_gateway'),
    path('payment/callback/<int:order_id>/', front.payment_callback, name='payment_callback'),
]

