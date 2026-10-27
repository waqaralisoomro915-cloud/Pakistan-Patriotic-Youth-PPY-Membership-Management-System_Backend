from rest_framework import serializers
from .models import Positions


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positions
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
    def validate(self, attrs):
        organization = attrs.get(
            "organization",
            self.instance.organization if self.instance else None
        )
        level = attrs.get(
            "level",
            self.instance.level if self.instance else None
        )
        if organization and level != organization.level:
            raise serializers.ValidationError({
                "level": "Position level must match the organization level."
            })

        return attrs