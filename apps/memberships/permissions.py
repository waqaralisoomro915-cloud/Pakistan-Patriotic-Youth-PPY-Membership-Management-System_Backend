
from rest_framework.permissions import BasePermission, SAFE_METHODS


class CanApplyForMembership(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.method in SAFE_METHODS
                or request.method == "POST"
                or request.user.is_staff
            )
        )


class CanManageMemberships(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )
