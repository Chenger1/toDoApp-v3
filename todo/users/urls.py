from django.urls import path

from .views import UserRegistrationView


app_name = 'users'

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='user_registration'),
]
