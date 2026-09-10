from django.urls import path
from core.views import front

app_name = 'core'

urlpatterns = [
    path('', front.home, name='home'),
    path('contact/', front.contact, name='contact'),
]
