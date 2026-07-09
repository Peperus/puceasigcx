from django.contrib import admin

from .models import Gradebook, GradeCalculationSnapshot, GradeItem, StudentGradeRecord


class GradeItemInline(admin.TabularInline):
    model = GradeItem
    extra = 0
    fields = ("parent", "item_type", "name", "order", "weight", "max_score")


@admin.register(Gradebook)
class GradebookAdmin(admin.ModelAdmin):
    list_display = (
        "course_section",
        "grading_model",
        "status",
        "opened_at",
        "closed_at",
    )
    list_filter = ("grading_model", "status")
    search_fields = (
        "course_section__subject__code",
        "course_section__subject__name",
        "course_section__parallel",
    )
    inlines = [GradeItemInline]


@admin.register(GradeItem)
class GradeItemAdmin(admin.ModelAdmin):
    list_display = ("gradebook", "item_type", "name", "order", "weight")
    list_filter = ("item_type", "gradebook__grading_model")
    search_fields = ("name", "gradebook__course_section__subject__code")


@admin.register(StudentGradeRecord)
class StudentGradeRecordAdmin(admin.ModelAdmin):
    list_display = ("course_enrollment", "grade_item", "score", "status", "updated_at")
    list_filter = ("status", "gradebook__grading_model")
    search_fields = (
        "course_enrollment__enrollment__student__student_code",
        "grade_item__name",
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(GradeCalculationSnapshot)
class GradeCalculationSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "course_enrollment",
        "grading_model",
        "final_score",
        "final_letter",
        "final_status",
        "is_current",
        "calculated_at",
    )
    list_filter = ("grading_model", "final_status", "is_current")
    search_fields = ("course_enrollment__enrollment__student__student_code",)
    readonly_fields = (
        "gradebook",
        "course_enrollment",
        "grading_model",
        "final_score",
        "final_letter",
        "final_status",
        "payload",
        "rule_version",
        "source",
        "calculated_by",
        "calculated_at",
        "is_current",
    )
