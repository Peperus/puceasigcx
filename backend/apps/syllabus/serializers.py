"""Serializers for syllabus API resources."""

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import (
    Syllabus,
    SyllabusAchievementLevel,
    SyllabusBibliography,
    SyllabusCompetency,
    SyllabusCriterion,
    SyllabusLearningOutcome,
    SyllabusWeeklyPlan,
)
from .services import model_validation_error_to_serializer_error, save_syllabus


class ServiceModelSerializer(serializers.ModelSerializer):
    save_service = None

    def _service_kwargs(self):
        request = self.context.get("request")
        return {
            "user": getattr(request, "user", None),
            "request": request,
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        try:
            if self.save_service is None:
                instance.save()
                return instance
            return self.save_service(instance, **self._service_kwargs())
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                model_validation_error_to_serializer_error(exc)
            ) from exc

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        try:
            if self.save_service is None:
                instance.save()
                return instance
            return self.save_service(instance, **self._service_kwargs())
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                model_validation_error_to_serializer_error(exc)
            ) from exc


class SyllabusSerializer(ServiceModelSerializer):
    course_label = serializers.SerializerMethodField()
    period_code = serializers.CharField(
        source="course_section.offer.period.code",
        read_only=True,
    )
    career_name = serializers.CharField(
        source="course_section.offer.career.name",
        read_only=True,
    )
    subject_code = serializers.CharField(
        source="course_section.subject.code",
        read_only=True,
    )
    subject_name = serializers.CharField(
        source="course_section.subject.name",
        read_only=True,
    )
    lead_teacher_name = serializers.CharField(
        source="lead_teacher.person.full_name",
        read_only=True,
    )
    co_teacher_name = serializers.CharField(
        source="co_teacher.person.full_name",
        read_only=True,
    )
    created_by_email = serializers.EmailField(source="created_by.email", read_only=True)
    approved_by_email = serializers.EmailField(
        source="approved_by.email", read_only=True
    )
    signed_file_uploaded_by_email = serializers.EmailField(
        source="signed_file_uploaded_by.email",
        read_only=True,
    )

    save_service = staticmethod(save_syllabus)

    class Meta:
        model = Syllabus
        fields = (
            "id",
            "course_section",
            "course_label",
            "period_code",
            "career_name",
            "subject_code",
            "subject_name",
            "version",
            "status",
            "subject_description",
            "methodology",
            "lead_teacher",
            "lead_teacher_name",
            "co_teacher",
            "co_teacher_name",
            "created_by",
            "created_by_email",
            "finalized_at",
            "submitted_at",
            "approved_at",
            "approved_by",
            "approved_by_email",
            "signed_file",
            "signed_file_uploaded_by",
            "signed_file_uploaded_by_email",
            "signed_file_uploaded_at",
            "archived_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "created_by",
            "finalized_at",
            "submitted_at",
            "approved_at",
            "approved_by",
            "signed_file",
            "signed_file_uploaded_by",
            "signed_file_uploaded_at",
            "archived_at",
            "created_at",
            "updated_at",
        )

    def get_course_label(self, obj):
        return str(obj.course_section)


class SyllabusCompetencySerializer(ServiceModelSerializer):
    class Meta:
        model = SyllabusCompetency
        fields = (
            "id",
            "syllabus",
            "competency_type",
            "text",
            "order",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class SyllabusLearningOutcomeSerializer(ServiceModelSerializer):
    class Meta:
        model = SyllabusLearningOutcome
        fields = (
            "id",
            "syllabus",
            "outcome_type",
            "code",
            "text",
            "order",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class SyllabusCriterionSerializer(ServiceModelSerializer):
    outcome_label = serializers.SerializerMethodField()

    class Meta:
        model = SyllabusCriterion
        fields = (
            "id",
            "syllabus",
            "learning_outcome",
            "outcome_label",
            "name",
            "description",
            "weight",
            "order",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def get_outcome_label(self, obj):
        return str(obj.learning_outcome)


class SyllabusAchievementLevelSerializer(ServiceModelSerializer):
    class Meta:
        model = SyllabusAchievementLevel
        fields = (
            "id",
            "criterion",
            "level",
            "description",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class SyllabusBibliographySerializer(ServiceModelSerializer):
    class Meta:
        model = SyllabusBibliography
        fields = (
            "id",
            "syllabus",
            "bibliography_type",
            "apa_reference",
            "library_code",
            "copies",
            "order",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class SyllabusWeeklyPlanSerializer(ServiceModelSerializer):
    outcome_label = serializers.SerializerMethodField()

    class Meta:
        model = SyllabusWeeklyPlan
        fields = (
            "id",
            "syllabus",
            "learning_outcome",
            "outcome_label",
            "week_number",
            "week_label",
            "start_date",
            "end_date",
            "knowledge_dimension",
            "contact_strategy",
            "contact_hours",
            "contact_resources",
            "contact_scenarios",
            "practical_strategy",
            "practical_hours",
            "practical_resources",
            "practical_scenarios",
            "autonomous_strategy",
            "autonomous_hours",
            "autonomous_resources",
            "autonomous_scenarios",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def get_outcome_label(self, obj):
        return str(obj.learning_outcome)
