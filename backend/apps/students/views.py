from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import BasePermission

from apps.accounts.roles import ROLE_STUDENT, user_has_role
from apps.audit.services import log_event

from .selectors import (
    user_can_manage_students,
    user_can_view_students_staff,
    visible_students_for_user,
)
from .serializers import StudentSerializer


def _student_snapshot(student):
    return {
        "id": student.pk,
        "person_id": student.person_id,
        "student_code": student.student_code,
        "career_id": student.career_id,
        "study_plan_id": student.study_plan_id,
        "status": student.status,
    }


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

    def perform_create(self, serializer):
        student = serializer.save()
        log_event(
            action="student_created",
            module="students",
            user=self.request.user,
            model_name="Student",
            object_id=student.pk,
            new_data=_student_snapshot(student),
            request=self.request,
        )

    def perform_update(self, serializer):
        previous = _student_snapshot(serializer.instance)
        student = serializer.save()
        log_event(
            action="student_updated",
            module="students",
            user=self.request.user,
            model_name="Student",
            object_id=student.pk,
            previous_data=previous,
            new_data=_student_snapshot(student),
            request=self.request,
        )

    def perform_destroy(self, instance):
        previous = _student_snapshot(instance)
        object_id = instance.pk
        instance.delete()
        log_event(
            action="student_deleted",
            module="students",
            user=self.request.user,
            model_name="Student",
            object_id=object_id,
            previous_data=previous,
            request=self.request,
        )
