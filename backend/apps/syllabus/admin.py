from django.contrib import admin

from .models import (
    Syllabus,
    SyllabusAchievementLevel,
    SyllabusBibliography,
    SyllabusCompetency,
    SyllabusCriterion,
    SyllabusLearningOutcome,
    SyllabusWeeklyPlan,
)


class SyllabusLearningOutcomeInline(admin.TabularInline):
    model = SyllabusLearningOutcome
    extra = 0


class SyllabusCompetencyInline(admin.TabularInline):
    model = SyllabusCompetency
    extra = 0


class SyllabusBibliographyInline(admin.TabularInline):
    model = SyllabusBibliography
    extra = 0


@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = (
        "course_section",
        "version",
        "status",
        "lead_teacher",
        "approved_at",
        "signed_file_uploaded_at",
    )
    list_filter = ("version", "status", "course_section__offer__period")
    search_fields = (
        "course_section__subject__code",
        "course_section__subject__name",
        "lead_teacher__person__first_name",
        "lead_teacher__person__last_name",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "finalized_at",
        "submitted_at",
        "approved_at",
        "signed_file_uploaded_at",
    )
    inlines = [
        SyllabusCompetencyInline,
        SyllabusLearningOutcomeInline,
        SyllabusBibliographyInline,
    ]


@admin.register(SyllabusCriterion)
class SyllabusCriterionAdmin(admin.ModelAdmin):
    list_display = ("learning_outcome", "name", "weight", "order")
    list_filter = ("learning_outcome__outcome_type",)
    search_fields = ("name", "learning_outcome__text")


@admin.register(SyllabusAchievementLevel)
class SyllabusAchievementLevelAdmin(admin.ModelAdmin):
    list_display = ("criterion", "level")
    list_filter = ("level",)
    search_fields = ("criterion__name", "description")


@admin.register(SyllabusWeeklyPlan)
class SyllabusWeeklyPlanAdmin(admin.ModelAdmin):
    list_display = (
        "syllabus",
        "week_number",
        "learning_outcome",
        "knowledge_dimension",
    )
    list_filter = ("syllabus__course_section__offer__period",)
    search_fields = (
        "week_label",
        "knowledge_dimension",
        "learning_outcome__text",
    )
