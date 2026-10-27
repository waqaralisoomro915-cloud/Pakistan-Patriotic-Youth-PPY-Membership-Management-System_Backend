from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from .models import Memberships
from .serializers import MembershipsSerializer
from .permissions import (CanApplyForMembership,CanManageMemberships,)
from .. import memberships


class MembershipViewSet(ModelViewSet):
    serializer_class = MembershipsSerializer
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Memberships.objects.all()
        else:
            return Memberships.objects.filter(user=user)
    def get_permissions(self):
        if self.action in ["create", "list", "retrieve"]:
            permission_classes = [CanApplyForMembership]
        else:
            permission_classes = [CanManageMemberships]

        return [permission() for permission in permission_classes]

