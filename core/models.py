import os

from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models
from core.managers import UserManager


class User(AbstractBaseUser):
    login = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=50)

    verification_token = models.CharField(max_length=32, null=True, blank=True, default=None)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['username',]

    objects = UserManager()

    def __str__(self):
        return f"{self.username}"

    def set_verification_token(self):
        code = os.urandom(16).hex()
        self.verification_token = code


class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text[:10]}...'
