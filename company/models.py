from django.db import models

from common.models import InvitationStatus, TimeStampedModel
from users.models import UserProfile, UserRequest


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


class Company(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(
        "users.UserProfile",
        on_delete=models.SET_NULL,
        null=True,
        related_name="owned_company",
    )
    is_visible = models.BooleanField(default=True)
    members = models.ManyToManyField(
        UserProfile, related_name="company_memberships", blank=True
    )
    invitations = models.ManyToManyField(
        Invitation, related_name="company_invitations", blank=True
    )
    user_requests = models.ManyToManyField(
        UserRequest, related_name="user_requests", blank=True
    )

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
