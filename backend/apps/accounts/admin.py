from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User, UserProfile


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    ordering = ("email",)
    list_display = (
        "email",
        "names",
        "last_names",
        "identification",
        "is_active",
        "is_staff",
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "groups")
    search_fields = ("email", "names", "last_names", "identification")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Datos institucionales",
            {"fields": ("names", "last_names", "identification", "phone")},
        ),
        (
            "Estado y permisos",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Fechas", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "names",
                    "last_names",
                    "identification",
                    "phone",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at", "last_login")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "primary_role",
        "must_change_password",
        "security_questions_configured",
        "is_active",
    )
    list_filter = (
        "primary_role",
        "must_change_password",
        "security_questions_configured",
        "is_active",
    )
    search_fields = ("user__email", "user__names", "user__last_names")
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at", "updated_at")
