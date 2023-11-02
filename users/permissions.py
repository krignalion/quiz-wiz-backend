from rest_framework import permissions


class IsInvitationReceiver(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.receiver == request.user


class IsRequestUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
