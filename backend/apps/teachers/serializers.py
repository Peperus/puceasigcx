"""Serializers for teachers API resources."""

from rest_framework import serializers

from .models import Teacher, TeacherOfficeHour


class TeacherOfficeHourSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source="get_day_of_week_display", read_only=True)

    class Meta:
        model = TeacherOfficeHour
        fields = (
            "id",
            "teacher",
            "modality",
            "day_of_week",
            "day_name",
            "start_time",
            "end_time",
            "location_or_link",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class TeacherSerializer(serializers.ModelSerializer):
    person_full_name = serializers.CharField(source="person.full_name", read_only=True)
    person_identification = serializers.CharField(
        source="person.identification_number",
        read_only=True,
    )
    institutional_email = serializers.EmailField(
        source="person.institutional_email",
        read_only=True,
    )
    domain_names = serializers.SerializerMethodField()
    office_hours = TeacherOfficeHourSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = (
            "id",
            "person",
            "person_full_name",
            "person_identification",
            "institutional_email",
            "teacher_code",
            "academic_degree",
            "professional_title",
            "academic_profile",
            "institutional_phone",
            "status",
            "domains",
            "domain_names",
            "office_hours",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def get_domain_names(self, obj):
        return [domain.name for domain in obj.domains.all()]
