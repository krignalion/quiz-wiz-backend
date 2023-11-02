from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    InvitationListViewSet,
    InvitedUsersView,
    UserListViewSet,
    UserRequestsView,
)

router = DefaultRouter()

router.register(r"invitations", InvitationListViewSet)
router.register(r"invited-users", InvitedUsersView, basename="invited-users")
router.register(r"user-requests", UserRequestsView, basename="user-requests")
router.register(r"", UserListViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "accept-invitation/<int:invitation_id>/",
        UserListViewSet.accept_invitation,
        name="accept-invitation",
    ),
    path(
        "send-request/<int:company_id>/",
        UserListViewSet.send_request,
        name="send-request",
    ),
    path(
        "cancel-request/<int:request_id>/",
        UserListViewSet.cancel_request,
        name="cancel-request",
    ),
    path(
        "approve-request/<int:request_id>/",
        UserListViewSet.approve_request,
        name="approve-request",
    ),
]
