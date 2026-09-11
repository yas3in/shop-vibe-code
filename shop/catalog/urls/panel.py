from django.urls import path

from catalog.views import panel

app_name = 'catalog_panel'

urlpatterns = [
    path('', panel.dashboard, name='dashboard'),
    path('products/', panel.panel_product_list, name='product_list'),
    path('products/create/', panel.panel_product_create, name='product_create'),
    path('products/<int:pk>/edit/', panel.panel_product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', panel.panel_product_delete, name='product_delete'),
]
