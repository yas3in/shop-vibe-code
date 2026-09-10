from django.urls import path
from catalog.views import panel

app_name = 'catalog'

urlpatterns = [
    path('', panel.dashboard, name='panel_dashboard'),
    path('products/', panel.panel_product_list, name='panel_product_list'),
    path('products/create/', panel.panel_product_create, name='panel_product_create'),
    path('products/<int:pk>/edit/', panel.panel_product_edit, name='panel_product_edit'),
    path('products/<int:pk>/delete/', panel.panel_product_delete, name='panel_product_delete'),
]
