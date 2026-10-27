from rest_framework import serializers
from .models import Memberships
class MembershipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memberships
        fields = "__all__"
        read_only_fields = [
            "id",
            "membership_number",
            "status",
            "applied_at",
            "reviewed_by",
            "reviewed_at",
            "rejection_reason",
            "joined_at",
            "created_at",
            "updated_at",
        ]
