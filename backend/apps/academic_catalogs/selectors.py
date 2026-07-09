"""Read/query helpers for academic catalogs domain."""

from apps.accounts.roles import (
    ROLE_ACADEMIC_DIRECTOR,
    ROLE_ADMINISTRATOR,
    ROLE_CAREER_COORDINATOR,
    ROLE_SECRETARY,
    user_has_role,
)


def user_can_manage_catalogs(user):
    return user_has_role(user, ROLE_ADMINISTRATOR, ROLE_SECRETARY)


def user_can_view_catalogs(user):
    return user_has_role(
        user,
        ROLE_ADMINISTRATOR,
        ROLE_SECRETARY,
        ROLE_CAREER_COORDINATOR,
        ROLE_ACADEMIC_DIRECTOR,
    )


def coordinator_career_ids(user):
    if user_has_role(user, ROLE_CAREER_COORDINATOR):
        return list(user.coordinated_careers.values_list("id", flat=True))
    return []


def user_is_career_coordinator(user):
    return user_has_role(user, ROLE_CAREER_COORDINATOR)
