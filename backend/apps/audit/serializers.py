"""Serializers for audit API resources."""

from rest_framework import serializers

from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = AuditLog
        fields = (
            "id",
            "created_at",
            "user",
            "user_email",
            "action",
            "module",
            "model_name",
            "object_id",
            "previous_data",
            "new_data",
            "reason",
            "ip_address",
            "user_agent",
        )
        read_only_fields = fields
