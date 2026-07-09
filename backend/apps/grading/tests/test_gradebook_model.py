import pytest
from django.core.exceptions import ValidationError

from apps.enrollment.models import CourseSectionStatus
from apps.grading.models import Gradebook, GradingModel
from apps.grading.tests.factories import (
    make_approved_syllabus,
    make_grading_syllabus,
    make_ready_course,
)


@pytest.mark.django_db
def test_gradebook_inherits_course_grading_model_and_requires_ready_syllabus():
    syllabus = make_approved_syllabus(code="GB1", grading_model=GradingModel.S1)

    gradebook = Gradebook.objects.create(
        course_section=syllabus.course_section,
        syllabus=syllabus,
    )

    assert gradebook.grading_model == GradingModel.S1
    assert gradebook.course_section.gradebook == gradebook


@pytest.mark.django_db
def test_gradebook_rejects_inactive_course():
    syllabus = make_approved_syllabus(code="GB2", grading_model=GradingModel.S2)
    syllabus.course_section.status = CourseSectionStatus.PLANNED
    syllabus.course_section.save()

    with pytest.raises(ValidationError):
        Gradebook.objects.create(
            course_section=syllabus.course_section,
            syllabus=syllabus,
        )


@pytest.mark.django_db
def test_gradebook_rejects_unapproved_syllabus():
    course_section = make_ready_course(code="GB3", grading_model=GradingModel.S3)
    syllabus = make_grading_syllabus(code="GB3", course_section=course_section)

    with pytest.raises(ValidationError):
        Gradebook.objects.create(course_section=course_section, syllabus=syllabus)
