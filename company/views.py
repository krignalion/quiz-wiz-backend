from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import RequestStatus, UserProfile, UserRequest

from .models import (
    Company,
    CompanyMember,
    Invitation,
    InvitationStatus,
    UserCompanyRole,
)
from .permissions import (
    CanRemoveUserFromCompany,
    CanSendInvitation,
    IsCompanyOwner,
    IsInvitationReceiver,
    IsInvitationSender,
)
from .serializers import (
    CompanyListSerializer,
    CompanyMemberSerializer,
    CompanySerializer,
    InvitationSerializer,
)


class CompanyPagination(PageNumberPagination):
    page_size = 10


def _save_invitation(invitation, status):
    invitation.status = status
    invitation.save()
    return Response({"message": f"Invitation {invitation.status} successfully"})


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = CompanyPagination
    permission_classes = [IsAuthenticated]

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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

    @api_view(["POST"])
    @permission_classes([CanSendInvitation])
    def send_invitation(request, company_id, user_id):
        company = get_object_or_404(Company, id=company_id)
        user = get_object_or_404(UserProfile, id=user_id)

        if company.members.filter(id=user.id).exists():
            return Response(
                {"message": "User is already a member of the company"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invitation = Invitation(sender=company.owner, receiver=user, company=company)
        invitation.save()

        return Response({"message": "Invitation sent successfully"})

    @api_view(["POST"])
    @permission_classes([IsInvitationSender])
    def revoke_invitation(self, invitation_id):
        invitation = get_object_or_404(Invitation, id=invitation_id)

        return _save_invitation(invitation, InvitationStatus.REVOKED)

    @api_view(["POST"])
    @permission_classes([IsInvitationReceiver])
    def reject_invitation(self, invitation_id):
        invitation = get_object_or_404(Invitation, id=invitation_id)

        return _save_invitation(invitation, InvitationStatus.REJECTED)

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
            if self.user not in invitation.company.members.all():
                invitation.status = InvitationStatus.APPROVED
                invitation.company.members.add(self.user)
                invitation.save()
                return Response(
                    {
                        "message": "Invitation accepted and user added to the company",
                        "invitation_status": InvitationStatus.APPROVED,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "User is already a member of the company"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {
                    "message": "Invitation is already " + invitation.status,
                    "invitation_status": invitation.status,
                },
                status=status.HTTP_400_BAD_REQUEST,
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


class CompanyMemberViewSet(viewsets.ModelViewSet):
    queryset = CompanyMember.objects.all()
    serializer_class = CompanyMemberSerializer

    @action(detail=True, methods=["POST"])
    def appoint_role(self, request, company_id=None):
        company = get_object_or_404(Company, id=company_id)

        if request.user != company.owner:
            return Response(
                "You do not have permission to appoint roles.",
                status=status.HTTP_403_FORBIDDEN,
            )

        user_id = request.data.get("user_id")
        status_role = request.data.get("status_role")

        if status_role not in [choice.value for choice in UserCompanyRole]:
            return Response(
                "Invalid status_role value.", status=status.HTTP_400_BAD_REQUEST
            )

        user = company.members.filter(id=user_id).first()

        if not user:
            return Response(
                f"User with id {user_id} is not a member of this company.",
                status=status.HTTP_404_NOT_FOUND,
            )

        user_role, created = CompanyMember.objects.get_or_create(
            user=user, company=company
        )
        user_role.role = status_role
        user_role.save()

        return Response("Role appointment completed.", status=status.HTTP_200_OK)
