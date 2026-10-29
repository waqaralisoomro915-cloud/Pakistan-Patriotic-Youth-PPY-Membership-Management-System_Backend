from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Card
from .serializers import CardSerializer


class CardViewSet(ModelViewSet):
    """
    API for authorized staff to issue and manage PPY cards.
    """

    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,]

    filterset_fields = [
        "card_type",
        "status",
        "organization",
        "membership",
        "position",
    ]

    search_fields = ["card_number","membership__membership_number",]
    ordering_fields = ["issued_at","expiration_date","created_at","card_number",]

    ordering = ["-created_at"]
    http_method_names = ["get","post","patch","head","options",]

    def get_queryset(self):
        """
        Staff can view cards. Other authenticated users see none.
        """
        queryset = Card.objects.select_related("membership","membership__user","position","organization",)

        if not self.request.user.is_staff:
            return queryset.none()
        return queryset

    def perform_create(self, serializer):
        """
        Only authorized staff can issue cards.
        """
        if not self.request.user.is_staff:
            raise PermissionDenied(
                "Only authorized staff can issue PPY cards."
            )
        with transaction.atomic():
            serializer.save()

    def perform_update(self, serializer):
        """
        Restrict card management to staff.
        """
        if not self.request.user.is_staff:
            raise PermissionDenied(
                "Only authorized staff can update PPY cards."
            )
        with transaction.atomic():
            serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        Cards should not be deleted through the API.
        Use a controlled revocation or replacement workflow instead.
        """
        raise PermissionDenied(
            "Cards cannot be deleted. Revoke or replace the card instead."
        )
