from django.urls import path

from orders.views import panel

app_name = 'orders_panel'

urlpatterns = [
    path('', panel.order_list, name='order_list'),
    path('<int:pk>/', panel.order_detail, name='order_detail'),
]
