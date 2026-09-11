from django.urls import path

from addresses.views import panel

app_name = 'addresses_panel'

urlpatterns = [
    path('', panel.address_list, name='address_list'),
]
