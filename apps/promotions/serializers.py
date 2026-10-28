
from rest_framework import serializers
from ..memberships.models import Memberships
from ..positions.models import Positions
from .models import Promotions


class PromotionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotions
        fields = "__all__"
        read_only_fields = [
            "id",
            "current_position",
            "status",
            "applied_at",
            "reviewed_by",
            "reviewed_at",
            "rejection_reason",
            "created_at",
            "updated_at",
        ]

    def validate_membership(self, membership):
        request = self.context.get("request")

        if membership.status != Memberships.Status.APPROVED:
            raise serializers.ValidationError(
                "Only approved members can apply for promotions."
            )

        if (
            request
            and request.user.is_authenticated
            and not request.user.is_staff
            and membership.user_id != request.user.id
        ):
            raise serializers.ValidationError(
                "You can apply only with your own membership."
            )

        if (
            self.instance
            and membership.pk != self.instance.membership_id
        ):
            raise serializers.ValidationError(
                "You cannot change the membership on an existing application."
            )

        return membership

    def validate_requested_position(self, position):
        if not position.is_active:
            raise serializers.ValidationError(
                "This position is inactive and cannot be requested."
            )
        return position

    def validate(self, attrs):
        request = self.context.get("request")

        if self.instance:
            if not request or not request.user.is_staff:
                raise serializers.ValidationError(
                    "Promotion applications cannot be edited by applicants."
                )

            if self.instance.status != Promotions.Status.PENDING:
                raise serializers.ValidationError(
                    "Only pending applications can be edited."
                )

        membership = attrs.get(
            "membership",
            self.instance.membership if self.instance else None,
        )
        position = attrs.get(
            "requested_position",
            self.instance.requested_position if self.instance else None,
        )

        if membership and position:
            duplicate = Promotions.objects.filter(
                membership=membership,
                requested_position=position,
                status=Promotions.Status.PENDING,
            )

            if self.instance:
                duplicate = duplicate.exclude(pk=self.instance.pk)

            if duplicate.exists():
                raise serializers.ValidationError({
                    "requested_position": (
                        "You already have a pending application for this position."
                    )
                })

        return attrs

    def create(self, validated_data):
        membership = validated_data["membership"]

        previous_approval = (
            Promotions.objects.filter(
                membership=membership,
                status=Promotions.Status.APPROVED,
            )
            .order_by("-reviewed_at", "-created_at")
            .first()
        )

        validated_data["current_position"] = (
            previous_approval.requested_position
            if previous_approval
            else None
        )

        return super().create(validated_data)
