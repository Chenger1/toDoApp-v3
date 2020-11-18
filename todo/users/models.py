from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    total_tasks = models.IntegerField(default=0)

