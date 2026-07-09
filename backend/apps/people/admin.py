from django.contrib import admin

from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "identification_number",
        "full_name",
        "institutional_email",
        "personal_email",
        "phone",
        "is_active",
    )
    list_filter = ("identification_type", "is_active")
    search_fields = (
        "identification_number",
        "first_name",
        "last_name",
        "institutional_email",
        "personal_email",
    )
    autocomplete_fields = ("user",)
    ordering = ("last_name", "first_name")
