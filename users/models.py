from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import TimeStampedModel, RequestStatus


class UserProfile(AbstractUser, TimeStampedModel):
    first_name = models.CharField(max_length=100, verbose_name="first name")
    last_name = models.CharField(max_length=100, verbose_name="last name")
    email = models.EmailField(unique=True, verbose_name="email address")
    password = models.CharField(max_length=128, verbose_name="password")
    image_path = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="avatar image path"
    )
    owned_companies = models.ManyToManyField("company.Company", related_name="owners")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserRequest(TimeStampedModel):
    user = models.ForeignKey(
        "users.UserProfile", on_delete=models.CASCADE, related_name="user_requests"
    )
    company = models.ForeignKey("company.Company", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=30,
        choices=[(status, status) for status in RequestStatus],
        default=RequestStatus.PENDING,
    )
