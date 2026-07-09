from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import BasePermission

from apps.accounts.roles import ROLE_STUDENT, user_has_role

from .selectors import (
    user_can_manage_students,
    user_can_view_students_staff,
    visible_students_for_user,
)
from .serializers import StudentSerializer


class CanReadOrManageStudents(BasePermission):
    def has_permission(self, request, view):
        if not getattr(request.user, "is_authenticated", False):
            return False
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return user_can_view_students_staff(request.user) or user_has_role(
                request.user,
                ROLE_STUDENT,
            )
        return user_can_manage_students(request.user)


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [CanReadOrManageStudents]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = (
        "student_code",
        "person__identification_number",
        "person__first_name",
        "person__last_name",
        "person__institutional_email",
        "career__name",
        "career__code",
    )
    ordering_fields = ("student_code", "person__last_name", "career__name")

    def get_queryset(self):
        return visible_students_for_user(self.request.user)
