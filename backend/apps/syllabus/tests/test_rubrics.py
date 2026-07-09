from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.syllabus.models import (
    AchievementLevelCode,
    LearningOutcomeType,
    SyllabusAchievementLevel,
    SyllabusCriterion,
)
from apps.syllabus.services import validate_rubrics_ready
from apps.syllabus.tests.factories import (
    add_complete_rubrics,
    add_required_learning_outcomes,
    make_syllabus,
)


@pytest.mark.django_db
def test_learning_outcomes_accept_criteria_and_achievement_levels():
    syllabus = make_syllabus("S5T3")
    add_required_learning_outcomes(syllabus)
    add_complete_rubrics(syllabus)

    validate_rubrics_ready(syllabus)

    first_criterion = SyllabusCriterion.objects.filter(syllabus=syllabus).first()
    assert first_criterion.achievement_levels.count() == 4


@pytest.mark.django_db
def test_rubric_weights_must_sum_one_hundred_per_subject_outcome():
    syllabus = make_syllabus("S5T3WEIGHT")
    add_required_learning_outcomes(syllabus)
    outcome = syllabus.syllabuslearningoutcomes.filter(
        outcome_type=LearningOutcomeType.SUBJECT
    ).first()
    criterion = SyllabusCriterion.objects.create(
        syllabus=syllabus,
        learning_outcome=outcome,
        name="Criterio incompleto",
        weight=Decimal("60.00"),
        order=1,
    )
    for level in AchievementLevelCode:
        SyllabusAchievementLevel.objects.create(
            criterion=criterion,
            level=level,
            description="Descriptor sintetico.",
        )

    with pytest.raises(ValidationError) as exc:
        validate_rubrics_ready(syllabus)

    assert "weight" in str(exc.value.message_dict)


@pytest.mark.django_db
def test_each_criterion_requires_levels_a_b_c_d():
    syllabus = make_syllabus("S5T3LEVELS")
    add_required_learning_outcomes(syllabus)
    outcome = syllabus.syllabuslearningoutcomes.filter(
        outcome_type=LearningOutcomeType.SUBJECT
    ).first()
    SyllabusCriterion.objects.create(
        syllabus=syllabus,
        learning_outcome=outcome,
        name="Criterio sin niveles",
        weight=Decimal("100.00"),
        order=1,
    )

    with pytest.raises(ValidationError) as exc:
        validate_rubrics_ready(syllabus)

    assert "levels" in str(exc.value.message_dict)
