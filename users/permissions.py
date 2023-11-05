from rest_framework import permissions


class IsOwnerOrReceiver(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or obj.receiver == request.user

    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return super().has_permission(request, view)


class IsRequestUser(IsOwnerOrReceiver):
    pass
