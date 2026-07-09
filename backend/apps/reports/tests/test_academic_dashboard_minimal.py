import pytest
from rest_framework.test import APIClient

from apps.enrollment.models import CourseEnrollment, TeachingAssignment, TeachingRole
from apps.enrollment.tests.factories import (
    make_course_section,
    make_enrollment,
    make_offer,
)
from apps.people.tests.factories import make_student, make_teacher, make_user


@pytest.mark.django_db
def test_academic_dashboard_returns_counts_by_period():
    user = make_user("secretaria-dashboard@example.edu", "USR-S4T7", "Secretaria")
    offer = make_offer("S4T7")
    section = make_course_section("S4T7", offer=offer)
    student = make_student(career=offer.career, student_code="EST-S4T7")
    enrollment = make_enrollment("S4T7", section, student)
    CourseEnrollment.objects.create(enrollment=enrollment, course_section=section)
    teacher = make_teacher(teacher_code="DOC-S4T7")
    TeachingAssignment.objects.create(
        course_section=section,
        teacher=teacher,
        role=TeachingRole.LEAD,
    )
    client = APIClient()
    client.force_authenticate(user)

    response = client.get(f"/api/academic/dashboard/?period={offer.period.code}")

    assert response.status_code == 200
    assert response.data["period"]["code"] == offer.period.code
    assert response.data["counts"] == {
        "students": 1,
        "teachers": 1,
        "courses": 1,
        "enrollments": 1,
    }


@pytest.mark.django_db
def test_academic_dashboard_limits_coordinator_to_assigned_career():
    coordinator = make_user(
        "coord-dashboard@example.edu",
        "USR-S4T7C",
        "Coordinador de carrera",
    )
    assigned_offer = make_offer("S4T7ASSIGNED")
    assigned_offer.career.coordinator_user = coordinator
    assigned_offer.career.save()
    visible_section = make_course_section("S4T7ASSIGNED", offer=assigned_offer)
    other_offer = make_offer("S4T7OTHER")
    other_offer.period = assigned_offer.period
    other_offer.save()
    other_section = make_course_section("S4T7OTHER", offer=other_offer)
    visible_enrollment = make_enrollment("S4T7ASSIGNED", visible_section)
    CourseEnrollment.objects.create(
        enrollment=visible_enrollment,
        course_section=visible_section,
    )
    other_enrollment = make_enrollment("S4T7OTHER", other_section)
    CourseEnrollment.objects.create(
        enrollment=other_enrollment,
        course_section=other_section,
    )
    client = APIClient()
    client.force_authenticate(coordinator)

    response = client.get(
        f"/api/academic/dashboard/?period={assigned_offer.period.code}"
    )

    assert response.status_code == 200
    assert response.data["counts"]["courses"] == 1
    assert response.data["counts"]["enrollments"] == 1


@pytest.mark.django_db
def test_academic_dashboard_rejects_unauthorized_roles():
    user = make_user("estudiante-dashboard@example.edu", "USR-S4T7S", "Estudiante")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/academic/dashboard/")

    assert response.status_code == 403
