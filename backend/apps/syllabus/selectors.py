"""Read/query helpers for syllabus domain."""

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
    Syllabus,
    SyllabusAchievementLevel,
    SyllabusBibliography,
    SyllabusCompetency,
    SyllabusCriterion,
    SyllabusLearningOutcome,
    SyllabusWeeklyPlan,
)

SYLLABUS_REVIEW_ROLES = (
    ROLE_ADMINISTRATOR,
    ROLE_SECRETARY,
    ROLE_CAREER_COORDINATOR,
    ROLE_ACADEMIC_DIRECTOR,
)


def user_can_view_syllabus_records(user):
    return user_has_role(user, *SYLLABUS_REVIEW_ROLES, ROLE_TEACHER, ROLE_STUDENT)


def user_can_create_syllabus_records(user):
    return user_has_role(user, ROLE_ADMINISTRATOR, ROLE_TEACHER)


def visible_syllabi_for_user(user):
    queryset = Syllabus.objects.select_related(
        "course_section",
        "course_section__offer",
        "course_section__offer__period",
        "course_section__offer__career",
        "course_section__subject",
        "lead_teacher",
        "lead_teacher__person",
        "co_teacher",
        "co_teacher__person",
        "created_by",
        "approved_by",
        "signed_file_uploaded_by",
    ).prefetch_related(
        "syllabuscompetencys",
        "syllabuslearningoutcomes",
        "syllabusbibliographys",
        "syllabusweeklyplans",
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
        return queryset.filter(
            course_section__course_enrollments__enrollment__student__person__user=user
        ).distinct()
    return queryset.none()


def _visible_children_for_user(user, model, *select_related):
    return model.objects.select_related("syllabus", *select_related).filter(
        syllabus_id__in=visible_syllabi_for_user(user).values("id")
    )


def visible_competencies_for_user(user):
    return _visible_children_for_user(user, SyllabusCompetency)


def visible_learning_outcomes_for_user(user):
    return _visible_children_for_user(user, SyllabusLearningOutcome)


def visible_criteria_for_user(user):
    return _visible_children_for_user(
        user,
        SyllabusCriterion,
        "learning_outcome",
    )


def visible_achievement_levels_for_user(user):
    return SyllabusAchievementLevel.objects.select_related(
        "criterion",
        "criterion__syllabus",
    ).filter(criterion__syllabus_id__in=visible_syllabi_for_user(user).values("id"))


def visible_bibliography_for_user(user):
    return _visible_children_for_user(user, SyllabusBibliography)


def visible_weekly_plans_for_user(user):
    return _visible_children_for_user(
        user,
        SyllabusWeeklyPlan,
        "learning_outcome",
    )
