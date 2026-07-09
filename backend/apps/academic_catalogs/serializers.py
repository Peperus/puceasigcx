"""Serializers for academic catalogs API resources."""

from rest_framework import serializers

from .models import (
    AcademicDomain,
    AcademicLevel,
    AcademicPeriod,
    AcademicSetting,
    AchievementLevel,
    Career,
    CurriculumPrerequisite,
    CurriculumSubject,
    FacultyOrUnit,
    GradingSystem,
    Modality,
    StudyPlan,
    Subject,
)


class AcademicPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicPeriod
        fields = "__all__"


class FacultyOrUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyOrUnit
        fields = "__all__"


class ModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Modality
        fields = "__all__"


class AcademicDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicDomain
        fields = "__all__"


class CareerSerializer(serializers.ModelSerializer):
    modality_name = serializers.CharField(source="modality.name", read_only=True)
    faculty_name = serializers.CharField(source="faculty.name", read_only=True)
    domain_name = serializers.CharField(source="domain.name", read_only=True)

    class Meta:
        model = Career
        fields = "__all__"


class StudyPlanSerializer(serializers.ModelSerializer):
    career_name = serializers.CharField(source="career.name", read_only=True)

    class Meta:
        model = StudyPlan
        fields = "__all__"


class AcademicLevelSerializer(serializers.ModelSerializer):
    study_plan_code = serializers.CharField(source="study_plan.code", read_only=True)

    class Meta:
        model = AcademicLevel
        fields = "__all__"


class GradingSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradingSystem
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    career_name = serializers.CharField(source="career.name", read_only=True)
    default_grading_system_code = serializers.CharField(
        source="default_grading_system.code",
        read_only=True,
    )

    class Meta:
        model = Subject
        fields = "__all__"


class CurriculumSubjectSerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source="subject.code", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    level_name = serializers.CharField(source="level.name", read_only=True)

    class Meta:
        model = CurriculumSubject
        fields = "__all__"


class CurriculumPrerequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumPrerequisite
        fields = "__all__"


class AchievementLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementLevel
        fields = "__all__"


class AcademicSettingSerializer(serializers.ModelSerializer):
    achievement_levels = AchievementLevelSerializer(many=True, read_only=True)
    default_grading_system_code = serializers.CharField(
        source="default_grading_system.code",
        read_only=True,
    )

    class Meta:
        model = AcademicSetting
        fields = "__all__"
