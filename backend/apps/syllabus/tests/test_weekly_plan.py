from datetime import date

import pytest
from django.core.exceptions import ValidationError

from apps.syllabus.models import LearningOutcomeType, SyllabusWeeklyPlan
from apps.syllabus.services import finalize_syllabus
from apps.syllabus.tests.factories import (
    add_complete_rubrics,
    add_minimum_bibliography,
    add_minimum_competency,
    add_minimum_weekly_plan,
    add_required_learning_outcomes,
    make_syllabus,
)


@pytest.mark.django_db
def test_syllabus_registers_weekly_plan_with_learning_experiences():
    syllabus = make_syllabus("S5T5")
    add_required_learning_outcomes(syllabus)

    weekly_plan = add_minimum_weekly_plan(syllabus)

    assert weekly_plan.week_number == 1
    assert weekly_plan.contact_hours > 0


@pytest.mark.django_db
def test_weekly_plan_rejects_invalid_dates_and_empty_experiences():
    syllabus = make_syllabus("S5T5BAD")
    add_required_learning_outcomes(syllabus)
    outcome = syllabus.syllabuslearningoutcomes.filter(
        outcome_type=LearningOutcomeType.SUBJECT
    ).first()

    with pytest.raises(ValidationError) as exc:
        SyllabusWeeklyPlan.objects.create(
            syllabus=syllabus,
            learning_outcome=outcome,
            week_number=1,
            start_date=date(2026, 2, 10),
            end_date=date(2026, 2, 1),
            knowledge_dimension="Conceptual",
        )

    assert "end_date" in exc.value.message_dict
    assert "contact_strategy" in exc.value.message_dict


@pytest.mark.django_db
def test_syllabus_cannot_finalize_without_minimum_weekly_plan():
    syllabus = make_syllabus("S5T5FINALIZE")
    add_minimum_competency(syllabus)
    add_required_learning_outcomes(syllabus)
    add_complete_rubrics(syllabus)
    add_minimum_bibliography(syllabus)

    with pytest.raises(ValidationError) as exc:
        finalize_syllabus(syllabus)

    assert "weekly_plan" in exc.value.message_dict
