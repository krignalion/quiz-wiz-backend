from django.db import models

from common.models import Invitation, TimeStampedModel, UserRequest
from users.models import UserProfile


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
    members = models.ManyToManyField(UserProfile, related_name="member_of", blank=True)
    invitations = models.ManyToManyField(
        Invitation, related_name="company_invitations", blank=True
    )
    requests = models.ManyToManyField(
        UserRequest, related_name="company_requests", blank=True
    )

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
