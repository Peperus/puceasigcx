"""Read/query helpers for people domain."""

from apps.accounts.roles import (
    ROLE_ACADEMIC_DIRECTOR,
    ROLE_ADMINISTRATOR,
    ROLE_CAREER_COORDINATOR,
    ROLE_SECRETARY,
    ROLE_STUDENT,
    ROLE_TEACHER,
    user_has_role,
)

from .models import Person

PEOPLE_MANAGER_ROLES = (ROLE_ADMINISTRATOR, ROLE_SECRETARY)
PEOPLE_STAFF_VIEW_ROLES = (
    ROLE_ADMINISTRATOR,
    ROLE_SECRETARY,
    ROLE_CAREER_COORDINATOR,
    ROLE_ACADEMIC_DIRECTOR,
)


def user_can_manage_people(user):
    return user_has_role(user, *PEOPLE_MANAGER_ROLES)


def user_can_view_people_staff(user):
    return user_has_role(user, *PEOPLE_STAFF_VIEW_ROLES)


def person_for_user(user):
    if not getattr(user, "is_authenticated", False):
        return None
    return Person.objects.filter(user=user).first()


def visible_people_for_user(user):
    queryset = Person.objects.select_related("user")
    if user_can_view_people_staff(user):
        return queryset
    if user_has_role(user, ROLE_TEACHER, ROLE_STUDENT):
        person = person_for_user(user)
        return queryset.filter(pk=person.pk) if person else queryset.none()
    return queryset.none()
