import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import UserProfile

logger = logging.getLogger(__name__)

@receiver(post_save, sender=UserProfile)
def user_profile_created(sender, instance, created, **kwargs):
    if created:
        logger.info(f'New user created: {instance}')

@receiver(post_save, sender=UserProfile)
def user_profile_updated(sender, instance, created, **kwargs):
    if not created:
        logger.info(f'User updated: {instance}')

@receiver(post_delete, sender=UserProfile)
def user_profile_deleted(sender, instance, **kwargs):
    logger.info(f'User deleted: {instance}')
