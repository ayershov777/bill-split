from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Group(models.Model):
    title: models.CharField(max_length=200)