from django.urls import path

from accounts.views import panel


urlpatterns = [
    path('', panel.profile, name='profile'),
]
