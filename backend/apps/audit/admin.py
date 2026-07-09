from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "module",
        "action",
        "user",
        "model_name",
        "object_id",
    )
    list_filter = ("module", "action", "created_at")
    search_fields = ("user__email", "model_name", "object_id", "reason")
    readonly_fields = (
        "user",
        "action",
        "module",
        "model_name",
        "object_id",
        "previous_data",
        "new_data",
        "reason",
        "ip_address",
        "user_agent",
        "created_at",
    )
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
