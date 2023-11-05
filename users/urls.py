from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    UserListViewSet,
    UserRequestsView,
)

router = DefaultRouter()
router.register(r"user-requests", UserRequestsView, basename="user-requests")
router.register(r"", UserListViewSet)

urlpatterns = [
    path("", include(router.urls)),
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
]
