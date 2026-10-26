
from rest_framework import serializers
from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "code",
            "level",
            "description",
            "parent",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        level = attrs.get(
            "level",
            self.instance.level if self.instance else None
        )

        parent = attrs.get(
            "parent",
            self.instance.parent if self.instance else None
        )

        expected_parent_levels = {
            Organization.Level.NATIONAL: None,
            Organization.Level.PROVINCE: Organization.Level.NATIONAL,
            Organization.Level.DISTRICT: Organization.Level.PROVINCE,
            Organization.Level.TEHSIL: Organization.Level.DISTRICT,
        }

        if level not in expected_parent_levels:
            raise serializers.ValidationError({
                "level": "Please select a valid organization level."
            })

        expected_parent = expected_parent_levels[level]

        if expected_parent is None and parent is not None:
            raise serializers.ValidationError({
                "parent": "National cannot have a parent."
            })

        if expected_parent is not None and parent is None:
            raise serializers.ValidationError({
                "parent": "This organization must have a parent."
            })

        if parent is not None and parent.level != expected_parent:
            raise serializers.ValidationError({
                "parent": f"This organization requires a {expected_parent} parent."
            })

        if (
            self.instance is not None
            and parent is not None
            and parent.pk == self.instance.pk
        ):
            raise serializers.ValidationError({
                "parent": "An organization cannot be its own parent."
            })

        return attrs
