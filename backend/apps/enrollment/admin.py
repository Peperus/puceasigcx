from django.contrib import admin

from .models import (
    AcademicOffer,
    CourseEnrollment,
    CourseSection,
    Enrollment,
    Homologation,
    TeachingAssignment,
)


@admin.register(AcademicOffer)
class AcademicOfferAdmin(admin.ModelAdmin):
    list_display = ("period", "career", "study_plan", "level", "status")
    list_filter = ("period", "career", "status")
    search_fields = ("period__code", "career__code", "career__name", "study_plan__code")
    autocomplete_fields = ("period", "career", "study_plan", "level")


@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "parallel",
        "offer",
        "capacity",
        "modality",
        "grading_system",
        "status",
    )
    list_filter = ("offer__period", "offer__career", "status", "modality")
    search_fields = ("subject__code", "subject__name", "parallel", "classroom")
    autocomplete_fields = ("offer", "subject", "modality", "grading_system")


@admin.register(TeachingAssignment)
class TeachingAssignmentAdmin(admin.ModelAdmin):
    list_display = ("course_section", "teacher", "role", "weekly_hours", "status")
    list_filter = ("role", "status", "course_section__offer__period")
    search_fields = (
        "course_section__subject__code",
        "course_section__subject__name",
        "teacher__teacher_code",
        "teacher__person__last_name",
    )
    autocomplete_fields = ("course_section", "teacher")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "period", "career", "study_plan", "status", "created_by")
    list_filter = ("period", "career", "status")
    search_fields = (
        "student__student_code",
        "student__person__first_name",
        "student__person__last_name",
    )
    autocomplete_fields = ("student", "period", "career", "study_plan", "created_by")


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "course_section", "status", "enrolled_at")
    list_filter = (
        "status",
        "course_section__offer__period",
        "course_section__offer__career",
    )
    search_fields = (
        "enrollment__student__student_code",
        "course_section__subject__code",
        "course_section__subject__name",
    )
    autocomplete_fields = ("enrollment", "course_section")


@admin.register(Homologation)
class HomologationAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "period", "status", "resolution_reference")
    list_filter = ("period", "status", "subject__career")
    search_fields = (
        "student__student_code",
        "student__person__last_name",
        "subject__code",
        "resolution_reference",
    )
    autocomplete_fields = ("student", "subject", "period", "registered_by")
