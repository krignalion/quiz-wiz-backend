from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class TimeStampedModel(models.Model):
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserProfile(AbstractUser, TimeStampedModel):
    first_name = models.CharField(max_length=100, verbose_name='first name')
    last_name = models.CharField(max_length=100, verbose_name='last name')
    email = models.EmailField(verbose_name='email address')
    password = models.CharField(max_length=128, verbose_name='password')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
