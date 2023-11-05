from django.shortcuts import get_object_or_404

from company.models import Company
from rest_framework import permissions
from users.models import UserProfile, UserRequest
from users.permissions import IsOwnerOrReceiver


class IsCompanyOwnerOrReadOnly(IsOwnerOrReceiver):
    pass


class CanSendInvitation(permissions.BasePermission):
    def has_permission(self, request, view):
        company_id = view.kwargs.get("company_id")

        company = get_object_or_404(Company, id=company_id)

        return request.user == company.owner


class CanApproveRequest(permissions.BasePermission):
    def has_permission(self, request, view):
        request_id = view.kwargs.get("request_id")
        request_obj = get_object_or_404(UserRequest, id=request_id)
        return request_obj.company.owner == request.user


class IsInvitationReceiver(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.receiver == request.user


class CanRemoveUserFromCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        company_id = view.kwargs.get("company_id")
        user_id = view.kwargs.get("user_id")

        company = get_object_or_404(Company, id=company_id)
        user = get_object_or_404(UserProfile, id=user_id)

        is_owner = request.user == company.owner
        is_user = request.user == user
        is_member = user in company.members.all()

        return is_owner or (is_user and is_member)
