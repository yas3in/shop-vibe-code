from django.urls import path
from orders.views import front

app_name = 'orders'

urlpatterns = [
    path('gateway/<int:order_id>/', front.payment_gateway, name='payment_gateway'),
    path('callback/<int:order_id>/', front.payment_callback, name='payment_callback'),
]
