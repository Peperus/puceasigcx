"""Read/query helpers for enrollment domain."""

from apps.academic_catalogs.selectors import coordinator_career_ids
from apps.accounts.roles import (
    ROLE_ACADEMIC_DIRECTOR,
    ROLE_ADMINISTRATOR,
    ROLE_CAREER_COORDINATOR,
    ROLE_SECRETARY,
    ROLE_STUDENT,
    ROLE_TEACHER,
    user_has_role,
)

from .models import (
    AcademicOffer,
    CourseEnrollment,
    CourseSection,
    Enrollment,
    Homologation,
    TeachingAssignment,
)

ENROLLMENT_MANAGER_ROLES = (ROLE_ADMINISTRATOR, ROLE_SECRETARY)
OFFER_MANAGER_ROLES = (
    ROLE_ADMINISTRATOR,
    ROLE_SECRETARY,
    ROLE_CAREER_COORDINATOR,
)
ACADEMIC_VIEW_ROLES = (
    ROLE_ADMINISTRATOR,
    ROLE_SECRETARY,
    ROLE_CAREER_COORDINATOR,
    ROLE_ACADEMIC_DIRECTOR,
)


def user_can_manage_enrollment_records(user):
    return user_has_role(user, *ENROLLMENT_MANAGER_ROLES)


def user_can_manage_offer_records(user):
    return user_has_role(user, *OFFER_MANAGER_ROLES)


def user_can_view_academic_offer(user):
    return user_has_role(user, *ACADEMIC_VIEW_ROLES, ROLE_TEACHER, ROLE_STUDENT)


def user_can_view_enrollment_records(user):
    return user_has_role(user, *ACADEMIC_VIEW_ROLES, ROLE_TEACHER, ROLE_STUDENT)


def user_can_manage_object_for_career(user, career_id):
    if user_has_role(user, ROLE_ADMINISTRATOR, ROLE_SECRETARY):
        return True
    if user_has_role(user, ROLE_CAREER_COORDINATOR):
        return career_id in coordinator_career_ids(user)
    return False


def visible_academic_offers_for_user(user):
    queryset = AcademicOffer.objects.select_related(
        "period",
        "career",
        "study_plan",
        "level",
    )
    if user_has_role(user, ROLE_ADMINISTRATOR, ROLE_SECRETARY, ROLE_ACADEMIC_DIRECTOR):
        return queryset
    if user_has_role(user, ROLE_CAREER_COORDINATOR):
        return queryset.filter(career_id__in=coordinator_career_ids(user))
    if user_has_role(user, ROLE_TEACHER):
        return queryset.filter(
            course_sections__teaching_assignments__teacher__person__user=user
        ).distinct()
    if user_has_role(user, ROLE_STUDENT):
        return queryset.filter(
            course_sections__course_enrollments__enrollment__student__person__user=user
        ).distinct()
    return queryset.none()


def visible_course_sections_for_user(user):
    queryset = CourseSection.objects.select_related(
        "offer",
        "offer__period",
        "offer__career",
        "offer__study_plan",
        "offer__level",
        "subject",
        "modality",
        "grading_system",
    ).prefetch_related("teaching_assignments")
    if user_has_role(user, ROLE_ADMINISTRATOR, ROLE_SECRETARY, ROLE_ACADEMIC_DIRECTOR):
        return queryset
    if user_has_role(user, ROLE_CAREER_COORDINATOR):
        return queryset.filter(offer__career_id__in=coordinator_career_ids(user))
    if user_has_role(user, ROLE_TEACHER):
        return queryset.filter(
            teaching_assignments__teacher__person__user=user
        ).distinct()
    if user_has_role(user, ROLE_STUDENT):
        return queryset.filter(
            course_enrollments__enrollment__student__person__user=user
        ).distinct()
    return queryset.none()


def visible_teaching_assignments_for_user(user):
    queryset = TeachingAssignment.objects.select_related(
        "course_section",
        "course_section__offer",
        "course_section__offer__period",
        "course_section__offer__career",
        "course_section__subject",
        "teacher",
        "teacher__person",
    )
    if user_has_role(user, ROLE_ADMINISTRATOR, ROLE_SECRETARY, ROLE_ACADEMIC_DIRECTOR):
        return queryset
    if user_has_role(user, ROLE_CAREER_COORDINATOR):
        return queryset.filter(
            course_section__offer__career_id__in=coordinator_career_ids(user)
        )
    if user_has_role(user, ROLE_TEACHER):
        return queryset.filter(teacher__person__user=user)
    return queryset.none()


def visible_enrollments_for_user(user):
    queryset = Enrollment.objects.select_related(
        "student",
        "student__person",
        "period",
        "career",
        "study_plan",
        "created_by",
    ).prefetch_related("course_enrollments")
    if user_has_role(user, ROLE_ADMINISTRATOR, ROLE_SECRETARY, ROLE_ACADEMIC_DIRECTOR):
        return queryset
    if user_has_role(user, ROLE_CAREER_COORDINATOR):
        return queryset.filter(career_id__in=coordinator_career_ids(user))
    if user_has_role(user, ROLE_TEACHER):
        return queryset.filter(
            course_enrollments__course_section__teaching_assignments__teacher__person__user=user
        ).distinct()
    if user_has_role(user, ROLE_STUDENT):
        return queryset.filter(student__person__user=user)
    return queryset.none()


def visible_course_enrollments_for_user(user):
    queryset = CourseEnrollment.objects.select_related(
        "enrollment",
        "enrollment__student",
        "enrollment__student__person",
        "course_section",
        "course_section__offer",
        "course_section__offer__period",
        "course_section__offer__career",
        "course_section__subject",
    )
    if user_has_role(user, ROLE_ADMINISTRATOR, ROLE_SECRETARY, ROLE_ACADEMIC_DIRECTOR):
        return queryset
    if user_has_role(user, ROLE_CAREER_COORDINATOR):
        return queryset.filter(
            course_section__offer__career_id__in=coordinator_career_ids(user)
        )
    if user_has_role(user, ROLE_TEACHER):
        return queryset.filter(
            course_section__teaching_assignments__teacher__person__user=user
        ).distinct()
    if user_has_role(user, ROLE_STUDENT):
        return queryset.filter(enrollment__student__person__user=user)
    return queryset.none()


def visible_homologations_for_user(user):
    queryset = Homologation.objects.select_related(
        "student",
        "student__person",
        "subject",
        "period",
        "registered_by",
    )
    if user_has_role(user, ROLE_ADMINISTRATOR, ROLE_SECRETARY, ROLE_ACADEMIC_DIRECTOR):
        return queryset
    if user_has_role(user, ROLE_CAREER_COORDINATOR):
        return queryset.filter(student__career_id__in=coordinator_career_ids(user))
    if user_has_role(user, ROLE_STUDENT):
        return queryset.filter(student__person__user=user)
    return queryset.none()
