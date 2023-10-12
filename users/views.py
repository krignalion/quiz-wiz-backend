import logging
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from users.models import UserProfile
from .serializers import UserProfileSerializer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

logger = logging.getLogger(__name__)

class UserProfilePagination(PageNumberPagination):
    page_size = 10

class UserListViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    pagination_class = UserProfilePagination
    queryset = UserProfile.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at']

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
