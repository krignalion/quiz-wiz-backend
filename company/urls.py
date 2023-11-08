from django.urls import include, path

from rest_framework.routers import DefaultRouter
from users.views import UserListViewSet

from .views import (
    CompanyMemberViewSet,
    CompanyViewSet,
    InvitationViewSet,
)

router = DefaultRouter()
router.register(r"", CompanyViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "send-invitation/<int:company_id>/<int:user_id>/",
        InvitationViewSet.send_invitation,
        name="send_invitation",
    ),
    path(
        "accept-invitation/<int:invitation_id>/",
        InvitationViewSet.accept_invitation,
        name="accept-invitation",
    ),
    path(
        "revoke-invitation/<int:invitation_id>/",
        InvitationViewSet.revoke_invitation,
        name="revoke_invitation",
    ),
    path(
        "reject-invitation/<int:invitation_id>/",
        InvitationViewSet.reject_invitation,
        name="reject_invitation",
    ),
    path(
        "<int:company_id>/remove-user/<int:user_id>/",
        InvitationViewSet.remove_user_from_company,
        name="remove-user-from-company",
    ),
    path(
        "approve-request/<int:request_id>/",
        UserListViewSet.approve_request,
        name="approve-request",
    ),
    path(
        "company-member/appoint-role/<int:company_id>/",
        CompanyMemberViewSet.as_view({"post": "appoint_role"}),
        name="company-member-appoint-role",
    ),
]
