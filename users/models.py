from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import TimeStampedModel


class UserProfile(AbstractUser, TimeStampedModel):
    first_name = models.CharField(max_length=100, verbose_name="first name")
    last_name = models.CharField(max_length=100, verbose_name="last name")
    email = models.EmailField(unique=True, verbose_name="email address")
    password = models.CharField(max_length=128, verbose_name="password")
    image_path = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="avatar image path"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
