from django.urls import path
from core.views import front

urlpatterns = [
    path('', front.home, name='home'),
    path('contact/', front.contact, name='contact'),
]

