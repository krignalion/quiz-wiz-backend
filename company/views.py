from django.shortcuts import get_object_or_404

from common.models import InvitationStatus
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import UserProfile

from .models import Company, Invitation
from .permissions import (
    CanRemoveUserFromCompany,
    CanSendInvitation,
    IsCompanyOwnerOrReadOnly,
    IsInvitationReceiver,
)
from .serializers import CompanyListSerializer, CompanySerializer, InvitationSerializer


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


class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

    @api_view(["POST"])
    @permission_classes([CanSendInvitation])
    def send_invitation(request, company_id, user_id):
        company = get_object_or_404(Company, id=company_id)
        user = get_object_or_404(UserProfile, id=user_id)

        invitation = Invitation(sender=company.owner, receiver=user, company=company)
        invitation.save()

        return Response({"message": "Invitation sent successfully"})

    @api_view(["POST"])
    def revoke_invitation(self, invitation_id):
        invitation = get_object_or_404(Invitation, id=invitation_id)

        if self.user == invitation.sender:
            invitation.status = InvitationStatus.REVOKED
            invitation.save()
            return Response({"message": "Invitation revoked successfully"})
        else:
            if self.user == invitation.receiver:
                invitation.status = InvitationStatus.REJECTED
                invitation.save()
                return Response({"message": "Invitation canceled successfully"})
            return Response({"message": "Permission denied"})

    @api_view(["POST"])
    @permission_classes([CanRemoveUserFromCompany])
    def remove_user_from_company(request, company_id, user_id):
        company = get_object_or_404(Company, id=company_id)
        user = get_object_or_404(UserProfile, id=user_id)

        company.members.remove(user)

        return Response({"message": "User removed from the company"})

    @api_view(["POST"])
    @permission_classes([IsInvitationReceiver])
    def accept_invitation(self, invitation_id):
        invitation = get_object_or_404(Invitation, id=invitation_id)

        if invitation.status == InvitationStatus.PENDING:
            invitation.status = InvitationStatus.APPROVED
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
