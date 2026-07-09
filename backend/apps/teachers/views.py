from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import BasePermission

from apps.accounts.roles import ROLE_TEACHER, user_has_role

from .selectors import (
    user_can_manage_teachers,
    user_can_view_teachers_staff,
    visible_office_hours_for_user,
    visible_teachers_for_user,
)
from .serializers import TeacherOfficeHourSerializer, TeacherSerializer


class CanReadOrManageTeachers(BasePermission):
    def has_permission(self, request, view):
        if not getattr(request.user, "is_authenticated", False):
            return False
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return user_can_view_teachers_staff(request.user) or user_has_role(
                request.user,
                ROLE_TEACHER,
            )
        return user_can_manage_teachers(request.user)


class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [CanReadOrManageTeachers]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = (
        "teacher_code",
        "person__identification_number",
        "person__first_name",
        "person__last_name",
        "person__institutional_email",
        "academic_degree",
        "professional_title",
        "domains__name",
    )
    ordering_fields = ("teacher_code", "person__last_name", "status")

    def get_queryset(self):
        return visible_teachers_for_user(self.request.user)


class TeacherOfficeHourViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherOfficeHourSerializer
    permission_classes = [CanReadOrManageTeachers]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = (
        "teacher__teacher_code",
        "teacher__person__first_name",
        "teacher__person__last_name",
        "location_or_link",
    )
    ordering_fields = ("day_of_week", "start_time", "teacher__teacher_code")

    def get_queryset(self):
        return visible_office_hours_for_user(self.request.user)
