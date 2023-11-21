from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from company.models import Company
from company.permissions import IsCompanyOwner
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from users.models import RequestStatus, UserProfile, UserRequest
from users.permissions import IsUserRequestUser

from .serializers import UserProfileSerializer


class UserProfilePagination(PageNumberPagination):
    page_size = 10


class UserListViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    pagination_class = UserProfilePagination
    queryset = UserProfile.objects.all().order_by("-created_at")

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["created_at"]

    @api_view(["POST"])
    @permission_classes([IsUserRequestUser])
    def cancel_request(self, request_id):
        request_obj = get_object_or_404(UserRequest, id=request_id)

        return _save_request(request_obj, RequestStatus.CANCELED)

    @api_view(["POST"])
    @permission_classes([IsCompanyOwner])
    def reject_request(self, request_id):
        request_obj = get_object_or_404(UserRequest, id=request_id)

        return _save_request(request_obj, RequestStatus.REJECTED)

    @api_view(["POST"])
    def send_request(request, company_id):
        user = request.user
        try:
            company = Company.objects.get(id=company_id)

            if company.members.filter(id=user.id).exists():
                return Response(
                    {"message": "User is already a member of the company"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            request_obj = UserRequest(
                user=user, company=company, status=RequestStatus.PENDING
            )
            request_obj.save()
            return Response(
                {"message": "Request sent successfully"}, status=status.HTTP_200_OK
            )
        except Company.DoesNotExist:
            return Response(
                {"detail": "Company not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @api_view(["POST"])
    @permission_classes([IsCompanyOwner])
    def approve_request(self, request_id):
        request = get_object_or_404(UserRequest, id=request_id)

        if request.company.members.filter(id=request.user.id).exists():
            return Response(
                {"message": "User is already a member of the company"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.company.members.add(request.user)
        request.status = RequestStatus.APPROVED
        request.save()
        return Response({"message": "Request approved"}, status=status.HTTP_200_OK)


def _save_request(request, status):
    request.status = status
    request.save()
    return Response({"message": f"Request {request.status} successfully"})
