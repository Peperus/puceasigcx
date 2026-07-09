"""Read/query helpers for students domain."""

from apps.academic_catalogs.selectors import coordinator_career_ids
from apps.accounts.roles import (
    ROLE_ACADEMIC_DIRECTOR,
    ROLE_ADMINISTRATOR,
    ROLE_CAREER_COORDINATOR,
    ROLE_SECRETARY,
    ROLE_STUDENT,
    user_has_role,
)

from .models import Student

STUDENT_MANAGER_ROLES = (ROLE_ADMINISTRATOR, ROLE_SECRETARY)
STUDENT_STAFF_VIEW_ROLES = (
    ROLE_ADMINISTRATOR,
    ROLE_SECRETARY,
    ROLE_CAREER_COORDINATOR,
    ROLE_ACADEMIC_DIRECTOR,
)


def user_can_manage_students(user):
    return user_has_role(user, *STUDENT_MANAGER_ROLES)


def user_can_view_students_staff(user):
    return user_has_role(user, *STUDENT_STAFF_VIEW_ROLES)


def visible_students_for_user(user):
    queryset = Student.objects.select_related(
        "person",
        "career",
        "study_plan",
        "admission_period",
    )
    if user_can_manage_students(user) or user_has_role(user, ROLE_ACADEMIC_DIRECTOR):
        return queryset
    if user_has_role(user, ROLE_CAREER_COORDINATOR):
        return queryset.filter(career_id__in=coordinator_career_ids(user))
    if user_has_role(user, ROLE_STUDENT):
        return queryset.filter(person__user=user)
    return queryset.none()
