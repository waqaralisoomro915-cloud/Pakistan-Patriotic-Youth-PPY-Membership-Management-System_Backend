from rest_framework import serializers
from .models import Audit
class AuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audit
        fields = "__all__"

        # Audit records must not be created or modified
        # directly by API clients.
        read_only_fields = (
            "id",
            "actor",
            "action",
            "target_type",
            "target_id",
            "timestamp",
            "details",
            "ip_address",
        )

    def validate_target_type(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Target type cannot be empty."
            )
        if len(value) > 100:
            raise serializers.ValidationError(
                "Target type cannot exceed 100 characters."
            )
        return value

    def validate_target_id(self, value):
        value = str(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Target ID cannot be empty."
            )
        if len(value) > 100:
            raise serializers.ValidationError(
                "Target ID cannot exceed 100 characters."
            )
        return value

    def validate_details(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError(
                "Details must be a JSON object."
            )
        return value
