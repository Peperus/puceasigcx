import pytest
from django.core.exceptions import ValidationError

from apps.syllabus.models import Syllabus, SyllabusStatus
from apps.syllabus.tests.factories import make_syllabus


@pytest.mark.django_db
def test_course_can_have_one_active_syllabus():
    syllabus = make_syllabus("S5T1")

    assert syllabus.course_section_id is not None
    assert syllabus.status == SyllabusStatus.DRAFT


@pytest.mark.django_db
def test_course_rejects_duplicate_active_syllabus():
    syllabus = make_syllabus("S5T1DUP")

    with pytest.raises(ValidationError):
        Syllabus.objects.create(
            course_section=syllabus.course_section,
            lead_teacher=syllabus.lead_teacher,
            subject_description="Duplicado sintetico.",
            methodology="Metodologia sintetica.",
        )


@pytest.mark.django_db
def test_course_allows_archived_history_and_new_active_syllabus():
    syllabus = make_syllabus("S5T1ARCH")
    syllabus.status = SyllabusStatus.ARCHIVED
    syllabus.save()

    new_syllabus = Syllabus.objects.create(
        course_section=syllabus.course_section,
        lead_teacher=syllabus.lead_teacher,
        subject_description="Nueva version sintetica.",
        methodology="Metodologia sintetica.",
    )

    assert new_syllabus.status == SyllabusStatus.DRAFT
