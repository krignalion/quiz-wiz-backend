import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Company
from .permissions import IsCompanyOwnerOrReadOnly
from .serializers import CompanyListSerializer, CompanySerializer


class CompanyPagination(PageNumberPagination):
    page_size = 10


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = CompanyPagination
    permission_classes = [IsAuthenticated, IsCompanyOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return CompanyListSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(is_visible=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Company)
def company_save(sender, instance, created, **kwargs):
    if created:
        instance.owner = instance.owner
        instance.save()
        logger.info(f"New company created: {instance}")
    else:
        logger.info(f"Company updated: {instance}")


@receiver(post_delete, sender=Company)
def company_deleted(sender, instance, **kwargs):
    logger.info(f"Company deleted: {instance}")
