from django.shortcuts import get_object_or_404

from company.models import UserCompanyRole
from rest_framework import permissions

from .models import Company


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        company_id = request.data.get("company")

        company = get_object_or_404(Company, id=company_id)
        if company.owner == request.user:
            return True

        is_admin = company.company_memberships.filter(
            user=request.user, role=UserCompanyRole.ADMIN
        ).exists()

        created_by_id = request.data.get("created_by")
        return is_admin and created_by_id == request.user.id

    def has_object_permission(self, request, view, obj):
        is_admin = obj.company.company_memberships.filter(
            user=request.user, role=UserCompanyRole.ADMIN
        ).exists()

        if obj.company.owner == request.user or is_admin:
            return True
        return False
