from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Promotions
from .serializers import PromotionsSerializer
from .permissions import (CanApplyForPromotion,CanManagePromotions,)


class PromotionViewSet(ModelViewSet):
    serializer_class = PromotionsSerializer
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        queryset = Promotions.objects.select_related(
            "membership",
            "membership__user",
            "current_position",
            "requested_position",
            "reviewed_by",
        )

        if self.request.user.is_staff:
            return queryset
        return queryset.filter(membership__user=self.request.user)

    def get_permissions(self):
        if self.action in [
            "create",
            "list",
            "retrieve",
            "metadata",
        ]:
            permission_classes = [CanApplyForPromotion]
        else:
            permission_classes = [CanManagePromotions]

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        with transaction.atomic():
            promotion = self.get_object()

            if promotion.status != Promotions.Status.PENDING:
                raise ValidationError(
                    "Only pending applications can be approved."
                )

            if promotion.membership.status != "approved":
                raise ValidationError(
                    "The membership must be approved first."
                )

            if not promotion.requested_position.is_active:
                raise ValidationError(
                    "This position is inactive."
                )

            promotion.status = Promotions.Status.APPROVED
            promotion.reviewed_by = request.user
            promotion.reviewed_at = timezone.now()
            promotion.rejection_reason = ""
            promotion.save(
                update_fields=[
                    "status",
                    "reviewed_by",
                    "reviewed_at",
                    "rejection_reason",
                    "updated_at",
                ]
            )

        return Response(
            PromotionsSerializer(
                promotion,
                context={"request": request},
            ).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        reason = request.data.get("rejection_reason", "").strip()

        if not reason:
            raise ValidationError({
                "rejection_reason": "A rejection reason is required."
            })

        with transaction.atomic():
            promotion = self.get_object()

            if promotion.status != Promotions.Status.PENDING:
                raise ValidationError(
                    "Only pending applications can be rejected."
                )

            promotion.status = Promotions.Status.REJECTED
            promotion.reviewed_by = request.user
            promotion.reviewed_at = timezone.now()
            promotion.rejection_reason = reason
            promotion.save(
                update_fields=[
                    "status",
                    "reviewed_by",
                    "reviewed_at",
                    "rejection_reason",
                    "updated_at",
                ]
            )

        return Response(
            PromotionsSerializer(
                promotion,
                context={"request": request},
            ).data,
            status=status.HTTP_200_OK,
        )
