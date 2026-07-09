from django.contrib import admin

from .models import Teacher, TeacherOfficeHour


class TeacherOfficeHourInline(admin.TabularInline):
    model = TeacherOfficeHour
    extra = 0
    fields = ("modality", "day_of_week", "start_time", "end_time", "location_or_link")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "teacher_code",
        "person",
        "academic_degree",
        "professional_title",
        "status",
    )
    list_filter = ("status", "domains")
    search_fields = (
        "teacher_code",
        "person__identification_number",
        "person__first_name",
        "person__last_name",
        "person__institutional_email",
        "academic_degree",
        "professional_title",
    )
    autocomplete_fields = ("person",)
    filter_horizontal = ("domains",)
    inlines = [TeacherOfficeHourInline]


@admin.register(TeacherOfficeHour)
class TeacherOfficeHourAdmin(admin.ModelAdmin):
    list_display = (
        "teacher",
        "modality",
        "day_of_week",
        "start_time",
        "end_time",
        "location_or_link",
    )
    list_filter = ("modality", "day_of_week", "teacher__status")
    search_fields = (
        "teacher__teacher_code",
        "teacher__person__first_name",
        "teacher__person__last_name",
        "location_or_link",
    )
    autocomplete_fields = ("teacher",)
