from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import BasePermission

from apps.accounts.roles import ROLE_TEACHER, user_has_role
from apps.audit.services import log_event

from .selectors import (
    user_can_manage_teachers,
    user_can_view_teachers_staff,
    visible_office_hours_for_user,
    visible_teachers_for_user,
)
from .serializers import TeacherOfficeHourSerializer, TeacherSerializer


def _teacher_snapshot(teacher):
    return {
        "id": teacher.pk,
        "person_id": teacher.person_id,
        "teacher_code": teacher.teacher_code,
        "status": teacher.status,
        "domain_ids": list(teacher.domains.order_by("id").values_list("id", flat=True)),
    }


def _office_hour_snapshot(office_hour):
    return {
        "id": office_hour.pk,
        "teacher_id": office_hour.teacher_id,
        "modality": office_hour.modality,
        "day_of_week": office_hour.day_of_week,
        "start_time": str(office_hour.start_time),
        "end_time": str(office_hour.end_time),
    }


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

    def perform_create(self, serializer):
        teacher = serializer.save()
        log_event(
            action="teacher_created",
            module="teachers",
            user=self.request.user,
            model_name="Teacher",
            object_id=teacher.pk,
            new_data=_teacher_snapshot(teacher),
            request=self.request,
        )

    def perform_update(self, serializer):
        previous = _teacher_snapshot(serializer.instance)
        teacher = serializer.save()
        log_event(
            action="teacher_updated",
            module="teachers",
            user=self.request.user,
            model_name="Teacher",
            object_id=teacher.pk,
            previous_data=previous,
            new_data=_teacher_snapshot(teacher),
            request=self.request,
        )

    def perform_destroy(self, instance):
        previous = _teacher_snapshot(instance)
        object_id = instance.pk
        instance.delete()
        log_event(
            action="teacher_deleted",
            module="teachers",
            user=self.request.user,
            model_name="Teacher",
            object_id=object_id,
            previous_data=previous,
            request=self.request,
        )


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

    def perform_create(self, serializer):
        office_hour = serializer.save()
        log_event(
            action="teacher_office_hour_created",
            module="teachers",
            user=self.request.user,
            model_name="TeacherOfficeHour",
            object_id=office_hour.pk,
            new_data=_office_hour_snapshot(office_hour),
            request=self.request,
        )

    def perform_update(self, serializer):
        previous = _office_hour_snapshot(serializer.instance)
        office_hour = serializer.save()
        log_event(
            action="teacher_office_hour_updated",
            module="teachers",
            user=self.request.user,
            model_name="TeacherOfficeHour",
            object_id=office_hour.pk,
            previous_data=previous,
            new_data=_office_hour_snapshot(office_hour),
            request=self.request,
        )

    def perform_destroy(self, instance):
        previous = _office_hour_snapshot(instance)
        object_id = instance.pk
        instance.delete()
        log_event(
            action="teacher_office_hour_deleted",
            module="teachers",
            user=self.request.user,
            model_name="TeacherOfficeHour",
            object_id=object_id,
            previous_data=previous,
            request=self.request,
        )
