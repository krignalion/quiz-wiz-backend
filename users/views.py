from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from common.models import RequestStatus
from company.models import Company
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import UserProfile, UserRequest
from company.permissions import CanApproveRequest

from .serializers import UserRequestSerializer, UserProfileSerializer


class UserProfilePagination(PageNumberPagination):
    page_size = 10


class UserListViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    pagination_class = UserProfilePagination
    queryset = UserProfile.objects.all().order_by("-created_at")

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["created_at"]

    @api_view(["POST"])
    def cancel_request(request, request_id):
        request_obj = get_object_or_404(UserRequest, id=request_id)

        if request.user == request_obj.company.owner:
            request_obj.status = RequestStatus.REJECTED
            request_obj.save()
            return Response({"message": "Request rejected successfully"})
        else:
            if request.user == request_obj.user:
                request_obj.status = RequestStatus.CANCELED
                request_obj.save()
                return Response(
                    {"message": "Request CANCELED successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
                )

    @api_view(["POST"])
    def send_request(request, company_id):
        user = request.user
        try:
            company = Company.objects.get(id=company_id)
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
    @permission_classes([CanApproveRequest])
    def approve_request(self, request_id):
        request = get_object_or_404(UserRequest, id=request_id)
        request.company.members.add(request.user)
        request.status = RequestStatus.APPROVED
        request.save()
        return Response({"message": "Request approved"}, status=status.HTTP_200_OK)


class UserRequestsView(viewsets.ModelViewSet):
    serializer_class = UserRequestSerializer

    def get_queryset(self):
        return UserRequest.objects.filter(user=self.request.user)

    @action(detail=False, methods=["GET"], url_path="request-for-joining")
    def request_for_joining(self, request):
        company_id = self.request.query_params.get("company_id")
        if company_id:
            company = get_object_or_404(Company, id=company_id)
            user = self.request.user
            if company.owner == user:
                queryset = UserRequest.objects.filter(company=company)
                serializer = UserRequestSerializer(queryset, many=True)
                return Response(serializer.data)
        return Response([])


class UserRequestViewSet(viewsets.ModelViewSet):
    queryset = UserRequest.objects.all()
    serializer_class = UserRequestSerializer
    permission_classes = [IsAuthenticated]
