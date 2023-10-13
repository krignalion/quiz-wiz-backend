import logging
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from users.models import UserProfile
from .serializers import UserProfileSerializer

logger = logging.getLogger(__name__)

class UserProfilePagination(PageNumberPagination):
    page_size = 10

class UserListViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    pagination_class = UserProfilePagination
    queryset = UserProfile.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at']
