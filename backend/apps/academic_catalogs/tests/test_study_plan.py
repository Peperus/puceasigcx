import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.academic_catalogs.models import AcademicLevel, StudyPlan
from apps.academic_catalogs.tests.factories import make_career, make_level, make_plan


@pytest.mark.django_db
def test_study_plan_has_ordered_levels():
    plan = make_plan(code="PLAN-A")
    level_1 = make_level(plan, number=1)
    level_2 = make_level(plan, number=2)

    assert list(plan.levels.order_by("order")) == [level_1, level_2]


@pytest.mark.django_db
def test_level_number_cannot_be_duplicated_per_plan():
    plan = make_plan(code="PLAN-A")
    make_level(plan, number=1)

    with pytest.raises(IntegrityError):
        AcademicLevel.objects.create(
            study_plan=plan,
            number=1,
            name="Nivel repetido",
            order=2,
        )


@pytest.mark.django_db
def test_only_one_current_plan_is_allowed_per_career():
    career = make_career(code="CUR")
    make_plan(career=career, code="PLAN-A")

    with pytest.raises(ValidationError):
        StudyPlan.objects.create(
            career=career,
            code="PLAN-B",
            name="Plan B",
            version="2027",
            effective_from="2027-01-01",
            is_current=True,
        )
