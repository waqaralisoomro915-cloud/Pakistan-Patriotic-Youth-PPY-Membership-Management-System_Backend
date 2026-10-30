
from rest_framework.permissions import BasePermission


class IsStaffUser(BasePermission):
    """
    Allows access only to authenticated staff users.
    """
    message = "Only staff members can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )

class IsOwnerOrStaff(BasePermission):
    """
    Allows staff users or the owner of an object.
    """

    message = "You do not have permission to access this object."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
        )
    def has_object_permission(self, request, view, obj):

        if request.user.is_staff:
            return True

        # Check whether the object belongs directly to the user.
        if hasattr(obj, "user_id"):
            return obj.user_id == request.user.id

        # Check ownership through a membership relationship.
        if hasattr(obj, "membership"):
            return obj.membership.user_id == request.user.id

        return False
