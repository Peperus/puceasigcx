import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.academic_catalogs.models import (
    CurriculumPrerequisite,
    CurriculumSubject,
    Subject,
)
from apps.academic_catalogs.tests.factories import (
    make_career,
    make_curriculum_subject,
    make_level,
    make_plan,
    make_subject,
)


@pytest.mark.django_db
def test_subject_can_be_registered_by_plan_and_level():
    plan = make_plan(code="PLAN-SUBJ")
    level = make_level(plan, number=1)
    subject = make_subject(plan.career, code="CAT-101")

    curriculum_subject = CurriculumSubject.objects.create(
        study_plan=plan,
        level=level,
        subject=subject,
        order=1,
    )

    assert curriculum_subject.study_plan == plan
    assert curriculum_subject.level == level
    assert curriculum_subject.subject == subject


@pytest.mark.django_db
def test_subject_code_is_unique_per_career():
    career = make_career(code="ENG")
    make_subject(career, code="MAT-101")

    with pytest.raises(IntegrityError):
        Subject.objects.create(
            career=career,
            code="MAT-101",
            name="Asignatura duplicada",
            total_hours=96,
            contact_hours=48,
            autonomous_hours=32,
            practical_hours=16,
        )


@pytest.mark.django_db
def test_curriculum_level_must_belong_to_study_plan():
    plan_a = make_plan(code="PLAN-A")
    plan_b = make_plan(career=make_career(code="ALT"), code="PLAN-B")
    level_b = make_level(plan_b, number=1)
    subject = make_subject(plan_a.career, code="CAT-102")

    with pytest.raises(ValidationError):
        CurriculumSubject.objects.create(
            study_plan=plan_a,
            level=level_b,
            subject=subject,
            order=1,
        )


@pytest.mark.django_db
def test_prerequisites_reject_simple_cycles():
    plan = make_plan(code="PLAN-PR")
    level_1 = make_level(plan, number=1)
    level_2 = make_level(plan, number=2)
    subject_1 = make_subject(plan.career, code="PR-101")
    subject_2 = make_subject(plan.career, code="PR-201")
    first = make_curriculum_subject(plan, level_1, subject_1, order=1)
    second = make_curriculum_subject(plan, level_2, subject_2, order=1)

    CurriculumPrerequisite.objects.create(
        curriculum_subject=second,
        prerequisite=first,
    )

    with pytest.raises(ValidationError):
        CurriculumPrerequisite.objects.create(
            curriculum_subject=first,
            prerequisite=second,
        )
