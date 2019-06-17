from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Group(models.Model):
    title = models.CharField(max_length=200)
    users = models.ManyToManyField(User)

class Payment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")
    amount = models.IntegerField()