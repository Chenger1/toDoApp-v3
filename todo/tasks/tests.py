from django.test import TestCase
from django.contrib.auth.models import User

from .models import Task


class TaskTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='test')
        Task.objects.create(title='second',
                            author=User.objects.get(username='test'),
                            )

    def test_title_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')
