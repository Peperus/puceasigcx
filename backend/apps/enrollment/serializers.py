"""Serializers for enrollment API resources."""

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import (
    AcademicOffer,
    CourseEnrollment,
    CourseSection,
    Enrollment,
    Homologation,
    TeachingAssignment,
)
from .services import (
    model_validation_error_to_serializer_error,
    save_academic_offer,
    save_course_enrollment,
    save_course_section,
    save_enrollment,
    save_homologation,
    save_teaching_assignment,
)


class ServiceModelSerializer(serializers.ModelSerializer):
    save_service = None
    audited = False

    def _service_kwargs(self):
        if not self.audited:
            return {}
        request = self.context.get("request")
        return {
            "user": getattr(request, "user", None),
            "request": request,
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        try:
            return self.save_service(instance, **self._service_kwargs())
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                model_validation_error_to_serializer_error(exc)
            ) from exc

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        try:
            return self.save_service(instance, **self._service_kwargs())
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                model_validation_error_to_serializer_error(exc)
            ) from exc


class AcademicOfferSerializer(ServiceModelSerializer):
    period_code = serializers.CharField(source="period.code", read_only=True)
    career_name = serializers.CharField(source="career.name", read_only=True)
    study_plan_code = serializers.CharField(source="study_plan.code", read_only=True)
    level_name = serializers.CharField(source="level.name", read_only=True)

    save_service = staticmethod(save_academic_offer)
    audited = True

    class Meta:
        model = AcademicOffer
        fields = (
            "id",
            "period",
            "period_code",
            "career",
            "career_name",
            "study_plan",
            "study_plan_code",
            "level",
            "level_name",
            "status",
            "description",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class CourseSectionSerializer(ServiceModelSerializer):
    period_code = serializers.CharField(source="offer.period.code", read_only=True)
    career_name = serializers.CharField(source="offer.career.name", read_only=True)
    subject_code = serializers.CharField(source="subject.code", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    modality_name = serializers.CharField(source="modality.name", read_only=True)
    grading_system_code = serializers.CharField(
        source="grading_system.code",
        read_only=True,
    )
    enrolled_count = serializers.IntegerField(read_only=True)
    available_seats = serializers.IntegerField(read_only=True)

    save_service = staticmethod(save_course_section)
    audited = True

    class Meta:
        model = CourseSection
        fields = (
            "id",
            "offer",
            "period_code",
            "career_name",
            "subject",
            "subject_code",
            "subject_name",
            "parallel",
            "capacity",
            "enrolled_count",
            "available_seats",
            "modality",
            "modality_name",
            "grading_system",
            "grading_system_code",
            "classroom",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class TeachingAssignmentSerializer(ServiceModelSerializer):
    course_label = serializers.SerializerMethodField()
    teacher_name = serializers.CharField(
        source="teacher.person.full_name", read_only=True
    )
    teacher_code = serializers.CharField(source="teacher.teacher_code", read_only=True)

    save_service = staticmethod(save_teaching_assignment)
    audited = True

    class Meta:
        model = TeachingAssignment
        fields = (
            "id",
            "course_section",
            "course_label",
            "teacher",
            "teacher_name",
            "teacher_code",
            "role",
            "weekly_hours",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def get_course_label(self, obj):
        return str(obj.course_section)


class EnrollmentSerializer(ServiceModelSerializer):
    student_code = serializers.CharField(source="student.student_code", read_only=True)
    student_name = serializers.CharField(
        source="student.person.full_name", read_only=True
    )
    period_code = serializers.CharField(source="period.code", read_only=True)
    career_name = serializers.CharField(source="career.name", read_only=True)
    study_plan_code = serializers.CharField(source="study_plan.code", read_only=True)
    created_by_email = serializers.EmailField(source="created_by.email", read_only=True)

    save_service = staticmethod(save_enrollment)
    audited = True

    class Meta:
        model = Enrollment
        fields = (
            "id",
            "student",
            "student_code",
            "student_name",
            "period",
            "period_code",
            "career",
            "career_name",
            "study_plan",
            "study_plan_code",
            "status",
            "created_by",
            "created_by_email",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_by", "created_at", "updated_at")


class CourseEnrollmentSerializer(ServiceModelSerializer):
    student_code = serializers.CharField(
        source="enrollment.student.student_code",
        read_only=True,
    )
    student_name = serializers.CharField(
        source="enrollment.student.person.full_name",
        read_only=True,
    )
    subject_code = serializers.CharField(
        source="course_section.subject.code",
        read_only=True,
    )
    course_label = serializers.SerializerMethodField()
    period_code = serializers.CharField(
        source="course_section.offer.period.code",
        read_only=True,
    )

    save_service = staticmethod(save_course_enrollment)
    audited = True

    class Meta:
        model = CourseEnrollment
        fields = (
            "id",
            "enrollment",
            "student_code",
            "student_name",
            "course_section",
            "course_label",
            "subject_code",
            "period_code",
            "status",
            "enrolled_at",
            "withdrawn_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("enrolled_at", "created_at", "updated_at")

    def get_course_label(self, obj):
        return str(obj.course_section)


class HomologationSerializer(ServiceModelSerializer):
    student_code = serializers.CharField(source="student.student_code", read_only=True)
    student_name = serializers.CharField(
        source="student.person.full_name", read_only=True
    )
    subject_code = serializers.CharField(source="subject.code", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    period_code = serializers.CharField(source="period.code", read_only=True)
    registered_by_email = serializers.EmailField(
        source="registered_by.email",
        read_only=True,
    )

    save_service = staticmethod(save_homologation)
    audited = True

    class Meta:
        model = Homologation
        fields = (
            "id",
            "student",
            "student_code",
            "student_name",
            "subject",
            "subject_code",
            "subject_name",
            "period",
            "period_code",
            "resolution_reference",
            "observations",
            "status",
            "registered_by",
            "registered_by_email",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("registered_by", "created_at", "updated_at")
