from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    UserListViewSet,
)

router = DefaultRouter()
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
    path(
        "reject-request/<int:request_id>/",
        UserListViewSet.reject_request,
        name="reject-request",
    ),
]
