from aenum import StrEnum, auto
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
        choices=[(status, status) for status in InvitationStatus],
        default=InvitationStatus.PENDING,
    )


class UserRequest(TimeStampedModel):
    user = models.ForeignKey(
        "users.UserProfile", on_delete=models.CASCADE, related_name="requests"
    )
    company = models.ForeignKey("company.Company", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=30,
        choices=[(status, status) for status in RequestStatus],
        default=RequestStatus.PENDING,
    )
