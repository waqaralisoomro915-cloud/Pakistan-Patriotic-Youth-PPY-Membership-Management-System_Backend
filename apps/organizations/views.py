from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import Organization
from .serializers import OrganizationSerializer


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.select_related("parent").all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdminUser]