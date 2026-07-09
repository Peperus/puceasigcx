import pytest
from django.core.exceptions import ValidationError

from apps.enrollment.models import (
    CourseEnrollment,
    CourseEnrollmentStatus,
    CourseSectionStatus,
    Enrollment,
    EnrollmentStatus,
)
from apps.enrollment.tests.factories import (
    make_course_section,
    make_enrollment,
    make_offer,
)
from apps.people.tests.factories import make_student


@pytest.mark.django_db
def test_student_can_have_period_enrollment_and_multiple_courses():
    offer = make_offer("S4T4")
    first_section = make_course_section("S4T4A", offer=offer)
    second_section = make_course_section("S4T4B", offer=offer)
    second_section.parallel = "B"
    second_section.save()
    student = make_student(career=offer.career, student_code="EST-S4T4")
    enrollment = Enrollment.objects.create(
        student=student,
        period=offer.period,
        career=student.career,
    )

    CourseEnrollment.objects.create(enrollment=enrollment, course_section=first_section)
    CourseEnrollment.objects.create(
        enrollment=enrollment, course_section=second_section
    )

    assert enrollment.status == EnrollmentStatus.ENROLLED
    assert enrollment.course_enrollments.count() == 2


@pytest.mark.django_db
def test_enrollment_rejects_duplicate_student_period():
    enrollment = make_enrollment("S4T4DUP")

    with pytest.raises(ValidationError):
        Enrollment.objects.create(
            student=enrollment.student,
            period=enrollment.period,
            career=enrollment.career,
        )


@pytest.mark.django_db
def test_course_enrollment_rejects_duplicate_course_for_student():
    section = make_course_section("S4T4COURSEDUP")
    enrollment = make_enrollment("S4T4COURSEDUP", section)
    CourseEnrollment.objects.create(enrollment=enrollment, course_section=section)

    with pytest.raises(ValidationError):
        CourseEnrollment.objects.create(enrollment=enrollment, course_section=section)


@pytest.mark.django_db
def test_course_enrollment_respects_capacity_for_active_courses():
    section = make_course_section("S4T4CAP", capacity=1)
    first_enrollment = make_enrollment("S4T4CAP1", section)
    second_student = make_student(
        career=section.offer.career, student_code="EST-S4T4CAP2"
    )
    second_enrollment = Enrollment.objects.create(
        student=second_student,
        period=section.offer.period,
        career=second_student.career,
    )
    CourseEnrollment.objects.create(
        enrollment=first_enrollment,
        course_section=section,
        status=CourseEnrollmentStatus.ENROLLED,
    )

    with pytest.raises(ValidationError):
        CourseEnrollment.objects.create(
            enrollment=second_enrollment,
            course_section=section,
            status=CourseEnrollmentStatus.ENROLLED,
        )


@pytest.mark.django_db
def test_course_enrollment_rejects_closed_course():
    section = make_course_section("S4T4CLOSED", status=CourseSectionStatus.CLOSED)
    enrollment = make_enrollment("S4T4CLOSED", section)

    with pytest.raises(ValidationError):
        CourseEnrollment.objects.create(enrollment=enrollment, course_section=section)
