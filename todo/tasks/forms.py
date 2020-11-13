from django import forms
from django.core.exceptions import ValidationError

from .models import Category


class CreateCategoryForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Category
        fields = ['name']

    def clean(self):
        super().clean()
        if Category.objects.filter(name=self.data['name'], author=self.user):
            raise ValidationError('This category already exists')
