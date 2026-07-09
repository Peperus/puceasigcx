from decimal import Decimal

from apps.grading.models import GradeFinalStatus
from apps.grading.services import calculate_s3_grade


def _partial(practice_score, evaluation_score):
    return {
        "practice_activities": [{"weight": 100, "score": practice_score}],
        "evaluation_score": evaluation_score,
    }


def test_s3_calculates_partials_and_approves_from_three_partials():
    result = calculate_s3_grade([_partial(40, 30), _partial(35, 35), _partial(45, 45)])

    assert result["partials"][0]["partial_score"] == 35
    assert result["preliminary_score"] == Decimal("38.33")
    assert result["final_status"] == GradeFinalStatus.APPROVED


def test_s3_requires_final_evaluation_when_partial_average_is_low():
    result = calculate_s3_grade([_partial(20, 20), _partial(25, 25), _partial(29, 29)])

    assert result["final_status"] == GradeFinalStatus.RECOVERY_REQUIRED
    assert result["recovery_required"] is True


def test_s3_successful_final_evaluation_approves_at_passing_score():
    result = calculate_s3_grade(
        [_partial(20, 20), _partial(25, 25), _partial(29, 29)],
        final_evaluation_score=35,
    )

    assert result["final_score"] == 30
    assert result["final_status"] == GradeFinalStatus.APPROVED
    assert result["recovery_required"] is False


def test_s3_failed_final_evaluation_fails_course():
    result = calculate_s3_grade(
        [_partial(20, 20), _partial(25, 25), _partial(29, 29)],
        final_evaluation_score=29,
    )

    assert result["final_status"] == GradeFinalStatus.FAILED
