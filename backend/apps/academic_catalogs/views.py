from rest_framework import viewsets
from rest_framework.permissions import BasePermission

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
from .selectors import (
    coordinator_career_ids,
    user_can_manage_catalogs,
    user_can_view_catalogs,
    user_is_career_coordinator,
)
from .serializers import (
    AcademicDomainSerializer,
    AcademicLevelSerializer,
    AcademicPeriodSerializer,
    AcademicSettingSerializer,
    AchievementLevelSerializer,
    CareerSerializer,
    CurriculumPrerequisiteSerializer,
    CurriculumSubjectSerializer,
    FacultyOrUnitSerializer,
    GradingSystemSerializer,
    ModalitySerializer,
    StudyPlanSerializer,
    SubjectSerializer,
)


class CanReadOrManageAcademicCatalogs(BasePermission):
    def has_permission(self, request, view):
        if not getattr(request.user, "is_authenticated", False):
            return False

        if request.method in ("GET", "HEAD", "OPTIONS"):
            return user_can_view_catalogs(request.user)

        return user_can_manage_catalogs(request.user)


class AcademicCatalogViewSet(viewsets.ModelViewSet):
    permission_classes = [CanReadOrManageAcademicCatalogs]


class AcademicPeriodViewSet(AcademicCatalogViewSet):
    queryset = AcademicPeriod.objects.all()
    serializer_class = AcademicPeriodSerializer
    search_fields = ("code", "name")
    ordering_fields = ("start_date", "end_date", "code")


class FacultyOrUnitViewSet(AcademicCatalogViewSet):
    queryset = FacultyOrUnit.objects.all()
    serializer_class = FacultyOrUnitSerializer
    search_fields = ("code", "name")


class ModalityViewSet(AcademicCatalogViewSet):
    queryset = Modality.objects.all()
    serializer_class = ModalitySerializer
    search_fields = ("code", "name")


class AcademicDomainViewSet(AcademicCatalogViewSet):
    queryset = AcademicDomain.objects.all()
    serializer_class = AcademicDomainSerializer
    search_fields = ("code", "name")


class CareerViewSet(AcademicCatalogViewSet):
    serializer_class = CareerSerializer
    search_fields = ("code", "name")

    def get_queryset(self):
        queryset = Career.objects.select_related(
            "faculty",
            "modality",
            "domain",
            "coordinator_user",
        )
        if user_can_manage_catalogs(self.request.user):
            return queryset
        if user_is_career_coordinator(self.request.user):
            return queryset.filter(id__in=coordinator_career_ids(self.request.user))
        return queryset


class StudyPlanViewSet(AcademicCatalogViewSet):
    serializer_class = StudyPlanSerializer
    search_fields = ("code", "name", "career__name")

    def get_queryset(self):
        queryset = StudyPlan.objects.select_related("career")
        if user_can_manage_catalogs(self.request.user):
            return queryset
        if user_is_career_coordinator(self.request.user):
            return queryset.filter(
                career_id__in=coordinator_career_ids(self.request.user)
            )
        return queryset


class AcademicLevelViewSet(AcademicCatalogViewSet):
    serializer_class = AcademicLevelSerializer
    search_fields = ("name", "study_plan__code", "study_plan__career__name")

    def get_queryset(self):
        queryset = AcademicLevel.objects.select_related(
            "study_plan", "study_plan__career"
        )
        if user_can_manage_catalogs(self.request.user):
            return queryset
        if user_is_career_coordinator(self.request.user):
            return queryset.filter(
                study_plan__career_id__in=coordinator_career_ids(self.request.user)
            )
        return queryset


class GradingSystemViewSet(AcademicCatalogViewSet):
    queryset = GradingSystem.objects.all()
    serializer_class = GradingSystemSerializer
    search_fields = ("code", "name")


class SubjectViewSet(AcademicCatalogViewSet):
    serializer_class = SubjectSerializer
    search_fields = ("code", "name", "career__name")

    def get_queryset(self):
        queryset = Subject.objects.select_related("career", "default_grading_system")
        if user_can_manage_catalogs(self.request.user):
            return queryset
        if user_is_career_coordinator(self.request.user):
            return queryset.filter(
                career_id__in=coordinator_career_ids(self.request.user)
            )
        return queryset


class CurriculumSubjectViewSet(AcademicCatalogViewSet):
    serializer_class = CurriculumSubjectSerializer
    search_fields = ("subject__code", "subject__name", "study_plan__code")

    def get_queryset(self):
        queryset = CurriculumSubject.objects.select_related(
            "study_plan",
            "study_plan__career",
            "level",
            "subject",
            "domain",
        )
        if user_can_manage_catalogs(self.request.user):
            return queryset
        if user_is_career_coordinator(self.request.user):
            return queryset.filter(
                study_plan__career_id__in=coordinator_career_ids(self.request.user)
            )
        return queryset


class CurriculumPrerequisiteViewSet(AcademicCatalogViewSet):
    serializer_class = CurriculumPrerequisiteSerializer

    def get_queryset(self):
        queryset = CurriculumPrerequisite.objects.select_related(
            "curriculum_subject",
            "curriculum_subject__study_plan",
            "curriculum_subject__study_plan__career",
            "prerequisite",
        )
        if user_can_manage_catalogs(self.request.user):
            return queryset
        if user_is_career_coordinator(self.request.user):
            return queryset.filter(
                curriculum_subject__study_plan__career_id__in=coordinator_career_ids(
                    self.request.user
                )
            )
        return queryset


class AcademicSettingViewSet(AcademicCatalogViewSet):
    serializer_class = AcademicSettingSerializer
    search_fields = ("name", "period__code", "career__code", "career__name")

    def get_queryset(self):
        queryset = AcademicSetting.objects.select_related(
            "period",
            "career",
            "default_grading_system",
        ).prefetch_related("achievement_levels")
        if user_can_manage_catalogs(self.request.user):
            return queryset
        if user_is_career_coordinator(self.request.user):
            return queryset.filter(
                career_id__in=coordinator_career_ids(self.request.user)
            ) | queryset.filter(career__isnull=True)
        return queryset


class AchievementLevelViewSet(AcademicCatalogViewSet):
    queryset = AchievementLevel.objects.select_related("setting")
    serializer_class = AchievementLevelSerializer
    search_fields = ("letter", "description", "setting__name")
