from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CompanyMembersView, CompanyViewSet

router = DefaultRouter()
router.register(r"company-members", CompanyMembersView, basename="company-members")
router.register(r"", CompanyViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "send-invitation/<int:company_id>/<int:user_id>/",
        CompanyViewSet.send_invitation,
        name="send_invitation",
    ),
    path(
        "revoke-invitation/<int:invitation_id>/",
        CompanyViewSet.revoke_invitation,
        name="revoke_invitation",
    ),
    path(
        "<int:company_id>/remove-user/<int:user_id>/",
        CompanyViewSet.remove_user_from_company,
        name="remove-user-from-company",
    ),
]
