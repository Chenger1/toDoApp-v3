from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation

from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as before, for verification.")

    class Meta:
        model = CustomUser
        fields = ('username',)

    def clean_password(self):
        password1 = self.cleaned_data.get['password1']
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Password don`t match')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
