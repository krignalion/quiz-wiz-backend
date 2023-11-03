from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from common.models import Invitation, InvitationStatus, RequestStatus, UserRequest
from company.models import Company
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import UserProfile

from .serializers import InvitationSerializer, RequestSerializer, UserProfileSerializer


class UserProfilePagination(PageNumberPagination):
    page_size = 10


class UserListViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    pagination_class = UserProfilePagination
    queryset = UserProfile.objects.all().order_by("-created_at")

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["created_at"]
    permission_classes = [IsAuthenticated]

    @api_view(["GET"])
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

    @api_view(["GET"])
    def accept_invitation(self, invitation_id):
        invitation = get_object_or_404(Invitation, id=invitation_id)

        if self.user == invitation.receiver:
            if invitation.status == InvitationStatus.PENDING.value:
                invitation.status = InvitationStatus.APPROVED.value
                invitation.save()

                invitation.company.members.add(self.user)
                return Response(
                    {"message": "Invitation accepted and user added to the company"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Invitation is already approved or rejected"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

    @api_view(["GET"])
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

    @api_view(["GET"])
    def approve_request(self, request_id):
        request = get_object_or_404(UserRequest, id=request_id)
        if self.user.id == request.company.owner.id:
            request.company.members.add(request.user)
            request.status = RequestStatus.APPROVED
            request.save()
            return Response({"message": "Request approved"}, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
        )


class UserRequestsView(viewsets.ModelViewSet):
    serializer_class = RequestSerializer

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
                serializer = RequestSerializer(queryset, many=True)
                return Response(serializer.data)
        return Response([])


class InvitationListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer


class InvitedUsersView(viewsets.ModelViewSet):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company_id = self.request.query_params.get("company_id")
        if company_id:
            company = get_object_or_404(Company, id=company_id)
            user = self.request.user
            if company.owner == user:
                queryset = Invitation.objects.filter(company=company)
                return queryset
        return Invitation.objects.none()
