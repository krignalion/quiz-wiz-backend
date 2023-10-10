import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import UserProfileFilter
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from users.models import UserProfile
from .serializers import UserProfileSerializer

logger = logging.getLogger(__name__)

class UserProfilePagination(PageNumberPagination):
    page_size = 10
    queryset = UserProfile.objects.all().order_by('id')

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserProfileFilter
    pagination_class = UserProfilePagination

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            # Logging an object deletion operation
            logger.info('Object deleted: {}'.format(instance))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            # Logging an error
            logger.error('Error deleting object: {}'.format(str(e)))
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='create-user')
    def create_user(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('New user created: {}'.format(serializer.data))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            logger.info('User updated: {}'.format(serializer.data))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateUserView(CreateAPIView):
    serializer_class = UserProfileSerializer
