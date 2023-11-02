from enum import Enum

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class InvitationStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    REVOKED = "Revoked"
    CANCELED = "Canceled"


class RequestStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    CANCELED = "Canceled"
    REVOKED = "Revoked"


class Invitation(TimeStampedModel):
    sender = models.ForeignKey(
        "users.UserProfile", on_delete=models.CASCADE, related_name="sent_invitations"
    )
    receiver = models.ForeignKey(
        "users.UserProfile",
        on_delete=models.CASCADE,
        related_name="received_invitations",
    )
    company = models.ForeignKey("company.Company", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=30,
        choices=[(status.name, status.value) for status in InvitationStatus],
        default=InvitationStatus.PENDING.value,
    )


class Request(TimeStampedModel):
    user = models.ForeignKey(
        "users.UserProfile", on_delete=models.CASCADE, related_name="requests"
    )
    company = models.ForeignKey("company.Company", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=30,
        choices=[(status.name, status.value) for status in RequestStatus],
        default=RequestStatus.PENDING.value,
    )
