from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwnerOrReadyOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.owner == request.user


class IsAdminUserOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super(
            IsAdminUserOrReadOnly, self
        ).has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin
