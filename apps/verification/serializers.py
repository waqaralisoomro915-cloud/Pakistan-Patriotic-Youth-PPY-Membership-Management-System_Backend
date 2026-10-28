from pathlib import Path
from rest_framework import serializers
from ..memberships.models import Memberships
from .models import Verification


class VerificationSerializer(serializers.ModelSerializer):
    MAX_FILE_SIZE = 5 * 1024 * 1024

    ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}

    class Meta:
        model = Verification
        fields = "__all__"
        read_only_fields = [
            "id",
            "status",
            "submitted_at",
            "reviewed_by",
            "reviewed_at",
            "rejection_reason",
            "review_notes",
            "created_at",
            "updated_at",
        ]

    def validate_membership(self, membership):
        request = self.context.get("request")

        if membership.status != Memberships.Status.PENDING:
            raise serializers.ValidationError(
                "Verification is only available for pending membership applications."
            )

        if request and request.user.is_authenticated:
            if (
                not request.user.is_staff
                and membership.user_id != request.user.id
            ):
                raise serializers.ValidationError(
                    "You can submit verification only for your own membership."
                )

        if self.instance and membership.pk != self.instance.membership_id:
            raise serializers.ValidationError(
                "You cannot change the membership linked to this verification."
            )

        return membership

    def validate_identity_document(self, file):
        return self.validate_document(file, "Identity document")

    def validate_police_verification_certificate(self, file):
        return self.validate_document(file, "Police verification certificate")

    def validate_document(self, file, label):
        extension = Path(file.name).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise serializers.ValidationError(
                f"{label} must be a PDF, JPG, JPEG, or PNG file."
            )

        if file.size > self.MAX_FILE_SIZE:
            raise serializers.ValidationError(
                f"{label} must not exceed 5 MB."
            )

        if file.size == 0:
            raise serializers.ValidationError(
                f"{label} cannot be empty."
            )

        return file

    def validate(self, attrs):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        is_staff = request.user.is_staff

        if self.instance:
            if not is_staff:
                if self.instance.membership.user_id != request.user.id:
                    raise serializers.ValidationError(
                        "You cannot modify another member's verification."
                    )

                if self.instance.status not in [
                    Verification.Status.REJECTED,
                    Verification.Status.RESUBMISSION_REQUIRED,
                ]:
                    raise serializers.ValidationError(
                        "You can only resubmit documents when resubmission is required."
                    )

            if "membership" in attrs:
                if attrs["membership"].pk != self.instance.membership_id:
                    raise serializers.ValidationError({
                        "membership": (
                            "The membership linked to this verification "
                            "cannot be changed."
                        )
                    })

        else:
            membership = attrs.get("membership")

            if membership is None:
                raise serializers.ValidationError({
                    "membership": "A membership application is required."
                })

            if not is_staff and membership.user_id != request.user.id:
                raise serializers.ValidationError({
                    "membership": (
                        "You can submit verification only for your own membership."
                    )
                })

            if Verification.objects.filter(
                membership=membership
            ).exists():
                raise serializers.ValidationError({
                    "membership": (
                        "A verification record already exists for this membership."
                    )
                })

        return attrs
