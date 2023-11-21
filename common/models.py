from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
