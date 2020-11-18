from django.db import models
from django.utils.text import slugify
from django.conf import settings

from time import time


def create_slug(title):
    slug = slugify(title, allow_unicode=True)
    return f'{slug}-{str(int(time()))}'


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150,
                            unique_for_date='created')

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='categories')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = create_slug(self.name)
        super().save(*args, **kwargs)


class Task(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=250,
                            unique_for_date='created')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='saved_tasks')

    description = models.TextField(max_length=250, blank=True)

    status = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category,
                                 related_name='categories',
                                 on_delete=models.CASCADE,)

    removed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = create_slug(self.title)
        super().save(*args, **kwargs)

    def get_model_name(self):
        return self.__class__.__name__


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

    def save(self, *args, **kwargs):
        if '-' not in self.slug:
            self.slug = create_slug(self.title)
        super().save(*args, **kwargs)

    def get_model_name(self):
        return self.__class__.__name__
