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
