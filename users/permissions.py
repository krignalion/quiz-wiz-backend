from django.shortcuts import get_object_or_404

from rest_framework import permissions
from users.models import UserRequest


class IsOwnerOrReceiver(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or obj.receiver == request.user

    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return super().has_permission(request, view)


class IsRequestUser(IsOwnerOrReceiver):
    pass


class IsUserRequestUser(permissions.BasePermission):
    def has_permission(self, request, view):
        request_id = view.kwargs.get("request_id")
        request_obj = get_object_or_404(UserRequest, id=request_id)
        return request_obj.user == request.user
