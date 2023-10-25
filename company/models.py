from django.db import models

from common.models import TimeStampedModel


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

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
