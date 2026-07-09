"""Read/query helpers for teachers domain."""

from apps.academic_catalogs.models import Career
from apps.academic_catalogs.selectors import coordinator_career_ids
from apps.accounts.roles import (
    ROLE_ACADEMIC_DIRECTOR,
    ROLE_ADMINISTRATOR,
    ROLE_CAREER_COORDINATOR,
    ROLE_SECRETARY,
    ROLE_TEACHER,
    user_has_role,
)

from .models import Teacher, TeacherOfficeHour

TEACHER_MANAGER_ROLES = (ROLE_ADMINISTRATOR, ROLE_SECRETARY)
TEACHER_STAFF_VIEW_ROLES = (
    ROLE_ADMINISTRATOR,
    ROLE_SECRETARY,
    ROLE_CAREER_COORDINATOR,
    ROLE_ACADEMIC_DIRECTOR,
)


def user_can_manage_teachers(user):
    return user_has_role(user, *TEACHER_MANAGER_ROLES)


def user_can_view_teachers_staff(user):
    return user_has_role(user, *TEACHER_STAFF_VIEW_ROLES)


def visible_teachers_for_user(user):
    queryset = Teacher.objects.select_related("person").prefetch_related(
        "domains",
        "office_hours",
    )
    if user_can_manage_teachers(user) or user_has_role(user, ROLE_ACADEMIC_DIRECTOR):
        return queryset
    if user_has_role(user, ROLE_CAREER_COORDINATOR):
        career_ids = coordinator_career_ids(user)
        domain_ids = Career.objects.filter(id__in=career_ids).values_list(
            "domain_id",
            flat=True,
        )
        return queryset.filter(domains__id__in=domain_ids).distinct()
    if user_has_role(user, ROLE_TEACHER):
        return queryset.filter(person__user=user)
    return queryset.none()


def visible_office_hours_for_user(user):
    return TeacherOfficeHour.objects.select_related(
        "teacher", "teacher__person"
    ).filter(teacher__in=visible_teachers_for_user(user))
