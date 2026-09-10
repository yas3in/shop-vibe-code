from django.urls import path
from catalog.views import front, panel

app_name = 'catalog'

urlpatterns = [
    path('', front.product_list, name='product_list'),
    path('<int:pk>/', front.product_detail, name='product_detail'),
    path('panel/', panel.dashboard, name='panel_dashboard'),
    path('panel/products/', panel.panel_product_list, name='panel_product_list'),
    path('panel/products/create/', panel.panel_product_create, name='panel_product_create'),
    path('panel/products/<int:pk>/edit/', panel.panel_product_edit, name='panel_product_edit'),
    path('panel/products/<int:pk>/delete/', panel.panel_product_delete, name='panel_product_delete'),
]

