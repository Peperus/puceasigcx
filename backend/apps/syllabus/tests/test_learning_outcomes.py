import pytest
from django.core.exceptions import ValidationError

from apps.syllabus.models import (
    CompetencyType,
    LearningOutcomeType,
    SyllabusCompetency,
    SyllabusLearningOutcome,
)
from apps.syllabus.services import validate_learning_outcomes_ready
from apps.syllabus.tests.factories import (
    add_required_learning_outcomes,
    make_syllabus,
)


@pytest.mark.django_db
def test_syllabus_registers_competencies_and_learning_outcomes():
    syllabus = make_syllabus("S5T2")

    competency = SyllabusCompetency.objects.create(
        syllabus=syllabus,
        competency_type=CompetencyType.DISCIPLINARY,
        text="Competencia disciplinar sintetica.",
        order=1,
    )
    outcomes = add_required_learning_outcomes(syllabus)

    assert competency.text
    assert len(outcomes) == 6
    assert (
        syllabus.syllabuslearningoutcomes.filter(
            outcome_type=LearningOutcomeType.SUBJECT
        ).count()
        == 3
    )


@pytest.mark.django_db
def test_learning_outcomes_require_three_career_and_subject_items():
    syllabus = make_syllabus("S5T2MIN")
    SyllabusLearningOutcome.objects.create(
        syllabus=syllabus,
        outcome_type=LearningOutcomeType.SUBJECT,
        text="Resultado incompleto sintetico.",
        order=1,
    )

    with pytest.raises(ValidationError) as exc:
        validate_learning_outcomes_ready(syllabus)

    assert "career" in exc.value.message_dict
    assert "subject" in exc.value.message_dict


@pytest.mark.django_db
def test_learning_outcomes_ready_with_minimum_required_items():
    syllabus = make_syllabus("S5T2READY")
    add_required_learning_outcomes(syllabus)

    validate_learning_outcomes_ready(syllabus)
