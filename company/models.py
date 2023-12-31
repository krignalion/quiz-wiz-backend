from enum import StrEnum, auto

from django.db import models

from common.models import TimeStampedModel
from users.models import UserProfile


class InvitationStatus(StrEnum):
    PENDING = auto()
    APPROVED = auto()
    REJECTED = auto()
    REVOKED = auto()


class UserCompanyRole(StrEnum):
    ADMIN = auto()
    USER = auto()


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

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class CompanyMember(TimeStampedModel):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="company_membership_members"
    )
    company = models.ForeignKey(
        "Company", related_name="company_memberships", on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=100, choices=[(role, role) for role in UserCompanyRole]
    )
