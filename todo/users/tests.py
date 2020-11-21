from django.test import TestCase
from django.contrib.auth import authenticate, login

from .models import CustomUser
from .forms import CustomUserCreationForm


class TaskTest(TestCase):

    def test_registration(self):
        form_data = {'username': 'test_user',
                     'password1': '12345678',
                     'password2': '12345678'}
        form = CustomUserCreationForm(form_data)
        self.assertTrue(form.is_valid())

    def test_user_auth_login_methods(self):
        form_data = {'username': 'test_user',
                     'password1': '12345678',
                     'password2': '12345678'}
        form = CustomUserCreationForm(form_data)
        if form.is_valid():
            cd = form.cleaned_data
            user = form.save()
            res = self.client.login(
                username=cd['username'],
                password=cd['password1']
            )
            self.assertTrue(res)
