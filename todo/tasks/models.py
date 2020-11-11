from django.db import models
from django.contrib.auth.models import User


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

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

