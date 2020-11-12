from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import UserRegistrationView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', UserRegistrationView.as_view(), name='user_registration'),
]
