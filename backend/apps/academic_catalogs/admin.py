from django.contrib import admin

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


@admin.register(AcademicPeriod)
class AcademicPeriodAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "status",
        "is_current",
        "start_date",
        "end_date",
    )
    list_filter = ("status", "is_current", "start_date", "end_date")
    search_fields = ("code", "name")
    ordering = ("-start_date", "code")


@admin.register(FacultyOrUnit)
class FacultyOrUnitAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "status")
    list_filter = ("status",)
    search_fields = ("code", "name")


@admin.register(Modality)
class ModalityAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "status")
    list_filter = ("status",)
    search_fields = ("code", "name")


@admin.register(AcademicDomain)
class AcademicDomainAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "status")
    list_filter = ("status",)
    search_fields = ("code", "name")


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "modality", "faculty", "domain", "status")
    list_filter = ("status", "modality", "faculty", "domain")
    search_fields = ("code", "name")
    autocomplete_fields = ("coordinator_user",)


class AcademicLevelInline(admin.TabularInline):
    model = AcademicLevel
    extra = 0
    fields = ("number", "name", "order")


@admin.register(StudyPlan)
class StudyPlanAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "career",
        "version",
        "is_current",
        "status",
        "effective_from",
    )
    list_filter = ("status", "is_current", "career")
    search_fields = ("code", "name", "career__name", "career__code")
    inlines = [AcademicLevelInline]


@admin.register(AcademicLevel)
class AcademicLevelAdmin(admin.ModelAdmin):
    list_display = ("study_plan", "number", "name", "order")
    list_filter = ("study_plan__career", "study_plan")
    search_fields = ("name", "study_plan__code", "study_plan__career__name")


@admin.register(GradingSystem)
class GradingSystemAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name")


class CurriculumPrerequisiteInline(admin.TabularInline):
    model = CurriculumPrerequisite
    fk_name = "curriculum_subject"
    extra = 0
    autocomplete_fields = ("prerequisite",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "career",
        "total_hours",
        "default_grading_system",
        "status",
    )
    list_filter = (
        "status",
        "career",
        "default_syllabus_version",
        "default_grading_system",
    )
    search_fields = ("code", "name", "career__name", "career__code")


@admin.register(CurriculumSubject)
class CurriculumSubjectAdmin(admin.ModelAdmin):
    list_display = ("study_plan", "level", "subject", "domain", "order", "credits")
    list_filter = (
        "study_plan__career",
        "study_plan",
        "level",
        "domain",
    )
    search_fields = (
        "study_plan__code",
        "subject__code",
        "subject__name",
        "level__name",
    )
    autocomplete_fields = ("study_plan", "level", "subject", "domain")
    inlines = [CurriculumPrerequisiteInline]


@admin.register(CurriculumPrerequisite)
class CurriculumPrerequisiteAdmin(admin.ModelAdmin):
    list_display = ("curriculum_subject", "prerequisite")
    search_fields = (
        "curriculum_subject__subject__code",
        "curriculum_subject__subject__name",
        "prerequisite__subject__code",
        "prerequisite__subject__name",
    )
    autocomplete_fields = ("curriculum_subject", "prerequisite")


class AchievementLevelInline(admin.TabularInline):
    model = AchievementLevel
    extra = 0
    fields = ("letter", "min_score", "max_score", "description")


@admin.register(AcademicSetting)
class AcademicSettingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "period",
        "career",
        "score_min",
        "score_max",
        "passing_score",
        "default_grading_system",
        "is_default",
    )
    list_filter = ("is_default", "period", "career", "default_grading_system")
    search_fields = ("name", "period__code", "career__code", "career__name")
    inlines = [AchievementLevelInline]


@admin.register(AchievementLevel)
class AchievementLevelAdmin(admin.ModelAdmin):
    list_display = ("setting", "letter", "min_score", "max_score", "description")
    list_filter = ("setting", "letter")
    search_fields = ("letter", "description", "setting__name")
