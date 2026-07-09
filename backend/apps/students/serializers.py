"""Serializers for students API resources."""

from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    person_full_name = serializers.CharField(source="person.full_name", read_only=True)
    person_identification = serializers.CharField(
        source="person.identification_number",
        read_only=True,
    )
    institutional_email = serializers.EmailField(
        source="person.institutional_email",
        read_only=True,
    )
    career_name = serializers.CharField(source="career.name", read_only=True)
    study_plan_code = serializers.CharField(source="study_plan.code", read_only=True)
    admission_period_code = serializers.CharField(
        source="admission_period.code",
        read_only=True,
    )

    class Meta:
        model = Student
        fields = (
            "id",
            "person",
            "person_full_name",
            "person_identification",
            "institutional_email",
            "student_code",
            "career",
            "career_name",
            "study_plan",
            "study_plan_code",
            "admission_period",
            "admission_period_code",
            "admission_date",
            "status",
            "observations",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")
