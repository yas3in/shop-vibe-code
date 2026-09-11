from django.urls import path

from catalog.views import front


urlpatterns = [
    path('', front.product_list, name='product_list'),
    path('<int:pk>/', front.product_detail, name='product_detail'),
]
