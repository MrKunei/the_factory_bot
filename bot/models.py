import os
from django.db import models
from core.models import User


class TgUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True, default=None)
    user = models.ForeignKey(User, models.PROTECT, null=True, default=None)
