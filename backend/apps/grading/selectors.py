"""Read/query helpers for grading domain."""

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
from apps.enrollment.models import (
    CourseEnrollment,
    CourseEnrollmentStatus,
    TeachingAssignmentStatus,
)

from .models import Gradebook, GradebookStatus

GRADEBOOK_STUDENT_VISIBLE_STATUSES = (
    GradebookStatus.OPEN,
    GradebookStatus.SUBMITTED,
    GradebookStatus.CLOSED,
    GradebookStatus.REOPENED,
)


def user_can_enter_grades(user):
    return user_has_role(user, ROLE_TEACHER)


def user_can_view_grade_reports(user):
    return user_has_role(
        user,
        ROLE_ADMINISTRATOR,
        ROLE_SECRETARY,
        ROLE_CAREER_COORDINATOR,
        ROLE_ACADEMIC_DIRECTOR,
    )


def user_can_manage_gradebook_closure(user):
    return user_has_role(
        user,
        ROLE_ADMINISTRATOR,
        ROLE_SECRETARY,
        ROLE_CAREER_COORDINATOR,
        ROLE_ACADEMIC_DIRECTOR,
    )


def user_can_export_grade_reports(user):
    return user_has_role(
        user,
        ROLE_ADMINISTRATOR,
        ROLE_SECRETARY,
        ROLE_CAREER_COORDINATOR,
        ROLE_ACADEMIC_DIRECTOR,
        ROLE_TEACHER,
    )


def teacher_gradebooks_for_user(user):
    return (
        Gradebook.objects.select_related(
            "course_section",
            "course_section__subject",
            "course_section__offer",
            "course_section__offer__period",
            "course_section__offer__career",
            "course_section__grading_system",
            "syllabus",
        )
        .filter(
            course_section__teaching_assignments__teacher__person__user=user,
            course_section__teaching_assignments__status=TeachingAssignmentStatus.ACTIVE,
        )
        .distinct()
    )


def user_can_edit_gradebook(user, gradebook):
    if gradebook.status not in {GradebookStatus.OPEN, GradebookStatus.REOPENED}:
        return False
    return teacher_gradebooks_for_user(user).filter(pk=gradebook.pk).exists()


def visible_gradebooks_for_reports(user):
    queryset = Gradebook.objects.select_related(
        "course_section",
        "course_section__subject",
        "course_section__offer",
        "course_section__offer__period",
        "course_section__offer__career",
        "course_section__grading_system",
        "syllabus",
    )
    if user_has_role(user, ROLE_ADMINISTRATOR, ROLE_SECRETARY, ROLE_ACADEMIC_DIRECTOR):
        return queryset
    if user_has_role(user, ROLE_CAREER_COORDINATOR):
        return queryset.filter(
            course_section__offer__career_id__in=coordinator_career_ids(user)
        )
    if user_has_role(user, ROLE_TEACHER):
        return queryset.filter(
            course_section__teaching_assignments__teacher__person__user=user,
            course_section__teaching_assignments__status=TeachingAssignmentStatus.ACTIVE,
        ).distinct()
    return queryset.none()


def student_course_enrollments_for_user(user):
    if not user_has_role(user, ROLE_STUDENT):
        return CourseEnrollment.objects.none()
    return CourseEnrollment.objects.select_related(
        "enrollment",
        "enrollment__student",
        "enrollment__student__person",
        "course_section",
        "course_section__subject",
        "course_section__offer",
        "course_section__offer__period",
        "course_section__offer__career",
        "course_section__gradebook",
    ).filter(
        enrollment__student__person__user=user,
        status=CourseEnrollmentStatus.ENROLLED,
        course_section__gradebook__status__in=GRADEBOOK_STUDENT_VISIBLE_STATUSES,
    )


def gradebook_course_enrollments(gradebook):
    return CourseEnrollment.objects.select_related(
        "enrollment",
        "enrollment__student",
        "enrollment__student__person",
        "course_section",
    ).filter(
        course_section=gradebook.course_section,
        status=CourseEnrollmentStatus.ENROLLED,
    )
