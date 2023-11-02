from django.shortcuts import get_object_or_404

from common.models import Invitation, InvitationStatus
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import UserProfile
from users.serializers import UserProfileSerializer

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

    @api_view(["GET", "POST"])
    def send_invitation(request, company_id, user_id):
        company = get_object_or_404(Company, id=company_id)
        user = get_object_or_404(UserProfile, id=user_id)

        if not request.user == company.owner:
            return Response(
                {"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        invitation = Invitation(sender=company.owner, receiver=user, company=company)
        invitation.save()

        return Response({"message": "Invitation sent successfully"})

    @api_view(["GET", "POST"])
    def revoke_invitation(self, invitation_id):
        invitation = get_object_or_404(Invitation, id=invitation_id)

        print("self.user:", self.user)
        print("invitation.sender:", invitation.sender)
        if self.user == invitation.sender:
            invitation.status = InvitationStatus.REVOKED.value
            invitation.save()
            return Response({"message": "Invitation revoked successfully"})
        else:
            if self.user == invitation.receiver:
                invitation.status = InvitationStatus.CANCELED.value
                invitation.save()
                return Response({"message": "Invitation canceled successfully"})
            return Response({"message": "Permission denied"})

    @api_view(["GET", "POST"])
    def remove_user_from_company(request, company_id, user_id):
        company = get_object_or_404(Company, id=company_id)
        user = get_object_or_404(UserProfile, id=user_id)

        if request.user == company.owner and user in company.members.all():
            company.members.remove(user)
            return Response({"message": "User removed from the company"})
        else:
            if request.user == user and user in company.members.all():
                company.members.remove(user)
                return Response({"message": "You left the company"})
            else:
                return Response(
                    {"message": "Permission denied or user is not in the company"}
                )


class CompanyMembersView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        company_id = self.request.query_params.get("company_id")
        try:
            company = Company.objects.get(id=company_id)
            return company.members.all()
        except Company.DoesNotExist:
            return UserProfile.objects.none()
