from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from users.models import UserProfile

from .serializers import UserProfileSerializer


class UserProfilePagination(PageNumberPagination):
    page_size = 10


class UserListViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    pagination_class = UserProfilePagination
    queryset = UserProfile.objects.all().order_by("-created_at")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["created_at"]
    permission_classes = [IsAuthenticated]
