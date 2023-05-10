from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    country = models.CharField(max_length=100, null=False)  # Russia
    city = models.CharField(max_length=100, null=False)  # Kursk
    friends = models.ManyToManyField('self', blank=True)  # Отношения между пользователями
    outgoing_friend_requests = models.ManyToManyField(
        'self', symmetrical=False, related_name='incoming_friend_requests', blank=True)  # Отношения между пользователями
    def __str__(self):
        return self.username
# Create your models here.