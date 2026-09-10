from django.urls import path
from addresses.views import front

app_name = 'addresses'

urlpatterns = [
    path('', front.address_list, name='address_list'),
    path('create/', front.address_create, name='address_create'),
    path('<int:pk>/edit/', front.address_edit, name='address_edit'),
    path('<int:pk>/delete/', front.address_delete, name='address_delete'),
]

