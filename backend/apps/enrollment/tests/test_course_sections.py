import pytest
from django.core.exceptions import ValidationError

from apps.academic_catalogs.tests.factories import make_grading_system, make_subject
from apps.enrollment.models import CourseSection, CourseSectionStatus
from apps.enrollment.tests.factories import make_course_section, make_offer


@pytest.mark.django_db
def test_can_create_course_section_with_grading_system():
    section = make_course_section("S4T2")

    assert section.parallel == "A"
    assert section.status == CourseSectionStatus.ACTIVE
    assert section.grading_system.code.startswith("GS-")


@pytest.mark.django_db
def test_course_section_rejects_duplicate_subject_parallel_in_same_offer():
    section = make_course_section("S4T2DUP")

    with pytest.raises(ValidationError):
        CourseSection.objects.create(
            offer=section.offer,
            subject=section.subject,
            parallel=section.parallel,
            capacity=25,
            modality=section.modality,
            grading_system=section.grading_system,
        )


@pytest.mark.django_db
def test_course_section_requires_subject_from_offer_career():
    offer = make_offer("S4T2CAREER")
    other_subject = make_subject(code="SUB-S4T2-OTHER")

    with pytest.raises(ValidationError):
        CourseSection.objects.create(
            offer=offer,
            subject=other_subject,
            parallel="A",
            capacity=25,
            modality=offer.career.modality,
            grading_system=other_subject.default_grading_system,
        )


@pytest.mark.django_db
def test_course_section_requires_active_grading_system():
    offer = make_offer("S4T2GS")
    subject = make_subject(career=offer.career, code="SUB-S4T2GS")
    grading_system = make_grading_system("S4T2I")
    grading_system.is_active = False
    grading_system.save()

    with pytest.raises(ValidationError):
        CourseSection.objects.create(
            offer=offer,
            subject=subject,
            parallel="A",
            capacity=25,
            modality=offer.career.modality,
            grading_system=grading_system,
        )
