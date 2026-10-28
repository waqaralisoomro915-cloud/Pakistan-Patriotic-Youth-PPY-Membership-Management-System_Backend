
from rest_framework.permissions import BasePermission, SAFE_METHODS


class CanApplyForPromotion(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.method in SAFE_METHODS
                or request.method == "POST"
            )
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return obj.membership.user_id == request.user.id


class CanManagePromotions(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )
