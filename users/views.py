import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
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

    @staticmethod
    def handle_success_response(serializer, message, user=None):
        log_message = f'Success: {message}\nUser Data: {serializer.data}'
        if user:
            log_message += f'\nUser: {user.username} (ID: {user.id})'
        logger.info(log_message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def handle_error_response(serializer, message, status_code):
        logger.error(message)
        return Response(serializer.errors, status=status_code)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.handle_success_response(serializer, 'New user created')
        return self.handle_error_response(serializer, 'Error creating user', status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return self.create(request)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return self.handle_success_response(serializer, 'User updated')
        return self.handle_error_response(serializer, 'Error updating user', status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            logger.info('Object deleted: {}'.format(instance))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error('Error deleting object: {}'.format(str(e)))
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
