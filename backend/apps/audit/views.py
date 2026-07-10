from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from apps.accounts.roles import (
    ROLE_ACADEMIC_DIRECTOR,
    ROLE_ADMINISTRATOR,
    ROLE_CAREER_COORDINATOR,
    ROLE_SECRETARY,
    user_has_role,
)

from .models import AuditLog
from .serializers import AuditLogSerializer


class CanViewAuditLog(BasePermission):
    def has_permission(self, request, view):
        return bool(
            getattr(request.user, "is_authenticated", False)
            and user_has_role(
                request.user,
                ROLE_ADMINISTRATOR,
                ROLE_SECRETARY,
                ROLE_CAREER_COORDINATOR,
                ROLE_ACADEMIC_DIRECTOR,
            )
        )


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [CanViewAuditLog]

    def get_queryset(self):
        queryset = AuditLog.objects.select_related("user")
        filters = self.request.query_params
        exact_filters = {
            "module": filters.get("module"),
            "action": filters.get("action"),
            "model_name": filters.get("model_name"),
            "object_id": filters.get("object_id"),
            "user": filters.get("user"),
        }
        queryset = queryset.filter(
            **{key: value for key, value in exact_filters.items() if value}
        )
        if filters.get("user_email"):
            queryset = queryset.filter(user__email__icontains=filters["user_email"])
        if filters.get("created_from"):
            queryset = queryset.filter(created_at__date__gte=filters["created_from"])
        if filters.get("created_to"):
            queryset = queryset.filter(created_at__date__lte=filters["created_to"])
        return queryset
