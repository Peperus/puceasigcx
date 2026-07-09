import pytest
from django.core.exceptions import ValidationError

from apps.enrollment.models import TeachingAssignment, TeachingRole
from apps.enrollment.selectors import visible_course_sections_for_user
from apps.enrollment.tests.factories import make_active_teacher, make_course_section
from apps.people.tests.factories import make_person, make_teacher, make_user
from apps.teachers.models import TeacherStatus


@pytest.mark.django_db
def test_course_can_have_lead_teacher_and_co_teacher():
    section = make_course_section("S4T3")
    lead = make_active_teacher("S4T3LEAD")
    co_teacher = make_active_teacher("S4T3CO")

    TeachingAssignment.objects.create(
        course_section=section,
        teacher=lead,
        role=TeachingRole.LEAD,
    )
    TeachingAssignment.objects.create(
        course_section=section,
        teacher=co_teacher,
        role=TeachingRole.CO_TEACHER,
    )

    assert section.teaching_assignments.count() == 2


@pytest.mark.django_db
def test_teaching_assignment_requires_active_teacher():
    section = make_course_section("S4T3INACTIVE")
    teacher = make_teacher(teacher_code="DOC-S4T3INACTIVE")
    teacher.status = TeacherStatus.INACTIVE
    teacher.save()

    with pytest.raises(ValidationError):
        TeachingAssignment.objects.create(
            course_section=section,
            teacher=teacher,
            role=TeachingRole.LEAD,
        )


@pytest.mark.django_db
def test_course_allows_only_one_active_lead_teacher():
    section = make_course_section("S4T3UNIQUE")
    lead = make_active_teacher("S4T3U1")
    other_lead = make_active_teacher("S4T3U2")
    TeachingAssignment.objects.create(
        course_section=section,
        teacher=lead,
        role=TeachingRole.LEAD,
    )

    with pytest.raises(ValidationError):
        TeachingAssignment.objects.create(
            course_section=section,
            teacher=other_lead,
            role=TeachingRole.LEAD,
        )


@pytest.mark.django_db
def test_teacher_sees_only_assigned_courses():
    user = make_user("docente-s4t3@example.edu", "USR-S4T3", "Docente")
    teacher = make_teacher(
        person=make_person("PER-S4T3", user=user),
        teacher_code="DOC-S4T3",
    )
    assigned = make_course_section("S4T3VISIBLE")
    make_course_section("S4T3HIDDEN")
    TeachingAssignment.objects.create(
        course_section=assigned,
        teacher=teacher,
        role=TeachingRole.LEAD,
    )

    assert list(visible_course_sections_for_user(user)) == [assigned]


@pytest.mark.django_db
def test_coordinator_sees_courses_from_assigned_career():
    coordinator = make_user(
        "coord-s4t3@example.edu", "USR-S4T3C", "Coordinador de carrera"
    )
    assigned = make_course_section("S4T3COORD")
    assigned.offer.career.coordinator_user = coordinator
    assigned.offer.career.save()
    make_course_section("S4T3OTHER")

    assert list(visible_course_sections_for_user(coordinator)) == [assigned]
