import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Company

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Company)
def company_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New company created: {instance}")
    else:
        logger.info(f"Company updated: {instance}")


@receiver(post_delete, sender=Company)
def company_deleted(sender, instance, **kwargs):
    logger.info(f"Company deleted: {instance}")
