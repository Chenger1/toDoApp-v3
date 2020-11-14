from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150,
                            unique_for_date='created')

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='categories')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=250,
                            unique_for_date='created')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='saved_tasks')

    description = models.TextField(max_length=250, blank=True)

    status = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category,
                                 related_name='categories',
                                 on_delete=models.CASCADE,)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Subtask(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250,
                            unique_for_date='created')

    task = models.ForeignKey(Task,
                             on_delete=models.CASCADE,
                             related_name='subtasks')

    status = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

