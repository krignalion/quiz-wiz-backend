from enum import StrEnum, auto

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class InvitationStatus(StrEnum):
    PENDING = auto()
    APPROVED = auto()
    REJECTED = auto()
    REVOKED = auto()


class RequestStatus(StrEnum):
    PENDING = auto()
    APPROVED = auto()
    REJECTED = auto()
    CANCELED = auto()
