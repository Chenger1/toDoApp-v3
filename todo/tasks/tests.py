from django.test import TestCase

from .models import Task, Category, Subtask
from .forms import CreateCategoryForm, CreateTaskForm

from users.models import CustomUser


class TaskTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create(username='test')
        category = Category.objects.create(name='test', author=user)
        task = Task.objects.create(title='second',
                                   author=user,
                                   category=category
                                   )
        Subtask.objects.create(title='subtask1', task=task)
        Subtask.objects.create(title='subtask2', task=task)

    def test_title_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_subtasks(self):
        task = Task.objects.get(id=1)
        Subtask.objects.create(title='subtask1', task=task)
        Subtask.objects.create(title='subtask2', task=task)
        self.assertEquals(task.subtasks.count(), 4)

    def test_mark_as_done(self):
        task = Task.objects.get(id=1)
        subtasks = task.subtasks.get_queryset()
        for subtask in subtasks:
            subtask.status = True
            subtask.save()
        task.check_subtasks()
        self.assertEquals(task.status, True)

    def test_task_form(self):
        user = CustomUser.objects.get(id=1)
        category = Category.objects.get(id=1)
        form_data = {'title': 'test_form',
                     'description': 'Test description',
                     'category': category,
                     'author': user}
        form = CreateTaskForm(user, form_data)
        self.assertTrue(form.is_valid())

    def test_category_form(self):
        user = CustomUser.objects.get(id=1)
        form_data = {'name': 'test_category',
                     'author': user}
        form = CreateCategoryForm(user, form_data)
        self.assertTrue(form.is_valid())
