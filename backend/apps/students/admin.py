from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_code",
        "person",
        "career",
        "study_plan",
        "admission_period",
        "status",
    )
    list_filter = ("status", "career", "study_plan", "admission_period")
    search_fields = (
        "student_code",
        "person__identification_number",
        "person__first_name",
        "person__last_name",
        "person__institutional_email",
    )
    autocomplete_fields = ("person", "career", "study_plan", "admission_period")
