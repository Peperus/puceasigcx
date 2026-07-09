from rest_framework.permissions import BasePermission

from apps.accounts.roles import (
    ACADEMIC_STAFF_ROLES,
    ROLE_ADMINISTRATOR,
    ROLE_CAREER_COORDINATOR,
    ROLE_SECRETARY,
    ROLE_STUDENT,
    ROLE_TEACHER,
    user_has_role,
)


class HasInstitutionalRole(BasePermission):
    required_roles = frozenset()

    def has_permission(self, request, view):
        user = request.user
        return bool(
            getattr(user, "is_authenticated", False)
            and user_has_role(user, *self.required_roles)
        )


class IsAdministrator(HasInstitutionalRole):
    required_roles = frozenset({ROLE_ADMINISTRATOR})


class IsSecretary(HasInstitutionalRole):
    required_roles = frozenset({ROLE_SECRETARY})


class IsCareerCoordinator(HasInstitutionalRole):
    required_roles = frozenset({ROLE_CAREER_COORDINATOR})


class IsTeacher(HasInstitutionalRole):
    required_roles = frozenset({ROLE_TEACHER})


class IsStudent(HasInstitutionalRole):
    required_roles = frozenset({ROLE_STUDENT})


class IsAcademicStaff(HasInstitutionalRole):
    required_roles = frozenset(ACADEMIC_STAFF_ROLES)
