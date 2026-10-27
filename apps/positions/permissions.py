
from rest_framework.permissions import BasePermission


class CanManagePositions(BasePermission):
    """
    Only Django staff users can manage positions.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )
