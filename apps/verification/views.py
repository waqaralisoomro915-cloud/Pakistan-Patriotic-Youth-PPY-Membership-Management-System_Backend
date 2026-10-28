
from django.db import transaction
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Verification
from .serializers import VerificationSerializer


class VerificationViewSet(ModelViewSet):
    serializer_class = VerificationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        queryset = Verification.objects.select_related(
            "membership",
            "membership__user",
            "reviewed_by",
        )

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(
            membership__user=self.request.user
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_update(self, serializer):
        if self.request.user.is_staff:
            raise PermissionDenied(
                "Use the review actions to update verification status."
            )

        serializer.save()

    def _get_pending_verification(self, pk):
        verification = self.get_object()

        if verification.status != Verification.Status.PENDING:
            raise ValidationError(
                "Only pending verifications can be reviewed."
            )

        return verification

    def _review(self, verification, status_value, reason=""):
        verification.status = status_value
        verification.reviewed_by = self.request.user
        verification.reviewed_at = timezone.now()
        verification.rejection_reason = reason

        verification.save(
            update_fields=[
                "status",
                "reviewed_by",
                "reviewed_at",
                "rejection_reason",
                "updated_at",
            ]
        )

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        if not request.user.is_staff:
            raise PermissionDenied(
                "Only authorized reviewers can approve verification."
            )

        with transaction.atomic():
            verification = self._get_pending_verification(pk)

            if not verification.identity_document:
                raise ValidationError(
                    "An identity document is required."
                )

            if not verification.police_verification_certificate:
                raise ValidationError(
                    "A police verification certificate is required."
                )

            self._review(
                verification,
                Verification.Status.APPROVED,
            )

        return Response(
            self.get_serializer(verification).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        if not request.user.is_staff:
            raise PermissionDenied(
                "Only authorized reviewers can reject verification."
            )

        reason = request.data.get("rejection_reason", "").strip()

        if not reason:
            raise ValidationError({
                "rejection_reason": "A rejection reason is required."
            })

        with transaction.atomic():
            verification = self._get_pending_verification(pk)

            self._review(
                verification,
                Verification.Status.REJECTED,
                reason,
            )

        return Response(
            self.get_serializer(verification).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def request_resubmission(self, request, pk=None):
        if not request.user.is_staff:
            raise PermissionDenied(
                "Only authorized reviewers can request resubmission."
            )

        reason = request.data.get("rejection_reason", "").strip()

        if not reason:
            raise ValidationError({
                "rejection_reason": (
                    "Explain which documents must be corrected."
                )
            })

        with transaction.atomic():
            verification = self._get_pending_verification(pk)

            self._review(
                verification,
                Verification.Status.RESUBMISSION_REQUIRED,
                reason,
            )

        return Response(
            self.get_serializer(verification).data,
            status=status.HTTP_200_OK,
        )
