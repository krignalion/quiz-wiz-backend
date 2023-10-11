from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
class UserProfile(TimeStampedModel):
    first_name = models.CharField(max_length=100, verbose_name='Name')
    last_name = models.CharField(max_length=100, verbose_name='Surname')
    email = models.EmailField(verbose_name='Email')
    password = models.CharField(max_length=128, verbose_name='Password')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
