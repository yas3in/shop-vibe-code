from django.urls import path
from accounts.views import front

app_name = 'accounts'

urlpatterns = [
    path('login/', front.login_view, name='login'),
    path('register/', front.register_view, name='register'),
    path('logout/', front.logout_view, name='logout'),
]
