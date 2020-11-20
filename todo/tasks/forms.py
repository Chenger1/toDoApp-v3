from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Task, Subtask


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


class CreateTaskForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(author=user)

    class Meta:
        model = Task
        fields = ['title', 'description', 'category']


class CreateSubTaskForm(forms.ModelForm):
    class Meta:
        model = Subtask
        fields = ['title']


CreateSubTaskFormSet = forms.inlineformset_factory(Task, Subtask,
                                                   form=CreateSubTaskForm, extra=2,
                                                   can_delete=False)
