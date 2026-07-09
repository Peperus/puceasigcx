import pytest
from rest_framework.test import APIClient

from apps.enrollment.models import (
    CourseEnrollment,
    CourseSectionStatus,
    TeachingAssignment,
    TeachingRole,
)
from apps.enrollment.tests.factories import (
    make_course_section,
    make_enrollment,
    make_offer,
)
from apps.people.tests.factories import (
    make_person,
    make_student,
    make_teacher,
    make_user,
)


@pytest.mark.django_db
def test_enrollment_api_requires_authentication():
    client = APIClient()

    response = client.get("/api/enrollment/course-sections/")

    assert response.status_code == 401


@pytest.mark.django_db
def test_secretary_can_create_course_enrollment_from_api():
    user = make_user("secretaria-s4t6@example.edu", "USR-S4T6", "Secretaria")
    section = make_course_section("S4T6CREATE")
    enrollment = make_enrollment("S4T6CREATE", section)
    client = APIClient()
    client.force_authenticate(user)

    response = client.post(
        "/api/enrollment/course-enrollments/",
        {
            "enrollment": enrollment.id,
            "course_section": section.id,
            "status": "enrolled",
        },
        format="json",
    )

    assert response.status_code == 201
    assert CourseEnrollment.objects.filter(enrollment=enrollment).exists()


@pytest.mark.django_db
def test_api_rejects_course_enrollment_in_closed_course():
    user = make_user("secretaria-s4t6-closed@example.edu", "USR-S4T6C", "Secretaria")
    section = make_course_section("S4T6CLOSED", status=CourseSectionStatus.CLOSED)
    enrollment = make_enrollment("S4T6CLOSED", section)
    client = APIClient()
    client.force_authenticate(user)

    response = client.post(
        "/api/enrollment/course-enrollments/",
        {
            "enrollment": enrollment.id,
            "course_section": section.id,
            "status": "enrolled",
        },
        format="json",
    )

    assert response.status_code == 400
    assert "course_section" in response.data


@pytest.mark.django_db
def test_teacher_reads_only_assigned_course_sections_from_api():
    user = make_user("docente-s4t6@example.edu", "USR-S4T6T", "Docente")
    teacher = make_teacher(
        person=make_person("PER-S4T6T", user=user),
        teacher_code="DOC-S4T6T",
    )
    assigned = make_course_section("S4T6ASSIGNED")
    make_course_section("S4T6HIDDEN")
    TeachingAssignment.objects.create(
        course_section=assigned,
        teacher=teacher,
        role=TeachingRole.LEAD,
    )
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/enrollment/course-sections/")

    assert response.status_code == 200
    assert [section["id"] for section in response.data] == [assigned.id]


@pytest.mark.django_db
def test_student_reads_only_own_course_enrollments_from_api():
    user = make_user("estudiante-s4t6@example.edu", "USR-S4T6S", "Estudiante")
    section = make_course_section("S4T6STUDENT")
    own_student = make_student(
        person=make_person("PER-S4T6S", user=user),
        career=section.offer.career,
        student_code="EST-S4T6S",
    )
    own_enrollment = make_enrollment("S4T6S", section, own_student)
    own_course_enrollment = CourseEnrollment.objects.create(
        enrollment=own_enrollment,
        course_section=section,
    )
    other_section = make_course_section("S4T6OTHERSTUDENT")
    other_enrollment = make_enrollment("S4T6OTHER", other_section)
    CourseEnrollment.objects.create(
        enrollment=other_enrollment,
        course_section=other_section,
    )
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/enrollment/course-enrollments/")

    assert response.status_code == 200
    assert [item["id"] for item in response.data] == [own_course_enrollment.id]


@pytest.mark.django_db
def test_coordinator_can_read_assigned_courses_but_cannot_enroll_students():
    coordinator = make_user(
        "coord-s4t6@example.edu", "USR-S4T6CO", "Coordinador de carrera"
    )
    offer = make_offer("S4T6COORD")
    offer.career.coordinator_user = coordinator
    offer.career.save()
    section = make_course_section("S4T6COORD", offer=offer)
    enrollment = make_enrollment("S4T6COORD", section)
    client = APIClient()
    client.force_authenticate(coordinator)

    list_response = client.get("/api/enrollment/course-sections/")
    create_response = client.post(
        "/api/enrollment/course-enrollments/",
        {
            "enrollment": enrollment.id,
            "course_section": section.id,
            "status": "enrolled",
        },
        format="json",
    )

    assert list_response.status_code == 200
    assert [item["id"] for item in list_response.data] == [section.id]
    assert create_response.status_code == 403
