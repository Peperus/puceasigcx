"""Serializers for people API resources."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        required=False,
        allow_null=True,
    )
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Person
        fields = (
            "id",
            "user",
            "user_email",
            "identification_type",
            "identification_number",
            "first_name",
            "last_name",
            "full_name",
            "institutional_email",
            "personal_email",
            "phone",
            "birth_date",
            "address",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")
