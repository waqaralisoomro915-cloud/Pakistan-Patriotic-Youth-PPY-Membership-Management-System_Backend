from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Audit
from .serializers import AuditSerializer


class AuditViewSet(ReadOnlyModelViewSet):
    """
    Read-only API for reviewing PPY audit history.

    Only authenticated staff users can access audit records.
    Audit records cannot be created, updated, or deleted through this API.
    """

    serializer_class = AuditSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Exact-match filters.
    filterset_fields = [
        "action",
        "target_type",
        "actor",
    ]

    # Text search.
    search_fields = [
        "target_type",
        "target_id",
    ]

    # Prevent arbitrary ordering fields.
    ordering_fields = [
        "timestamp",
        "action",
        "target_type",
    ]
    ordering = ["-timestamp"]

    http_method_names = ["get", "head", "options"]

    def get_queryset(self):
        user = self.request.user

        # Never expose audit history to non-staff users.
        if not user.is_authenticated or not user.is_staff:
            return Audit.objects.none()

        return Audit.objects.select_related("actor").all()
