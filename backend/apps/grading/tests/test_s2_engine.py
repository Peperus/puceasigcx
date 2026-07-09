from apps.grading.models import GradeFinalStatus
from apps.grading.services import calculate_s2_grade


def _outcome(score, recovery_score=None):
    data = {"criteria": [{"weight": 100, "score": score}]}
    if recovery_score is not None:
        data["recovery_score"] = recovery_score
    return data


def test_s2_approves_with_zero_failed_learning_outcomes():
    result = calculate_s2_grade([_outcome(30), _outcome(40), _outcome(45)])

    assert result["final_status"] == GradeFinalStatus.APPROVED
    assert result["failed_learning_outcomes_count"] == 0


def test_s2_one_failed_learning_outcome_requires_recovery():
    result = calculate_s2_grade([_outcome(29), _outcome(40), _outcome(45)])

    assert result["final_status"] == GradeFinalStatus.RECOVERY_REQUIRED
    assert result["recovery_required"] is True


def test_s2_successful_recovery_is_capped_at_passing_score():
    result = calculate_s2_grade([_outcome(29, 50), _outcome(40), _outcome(45)])
    recovered = result["learning_outcomes"][0]

    assert recovered["final_score"] == 30
    assert recovered["status"] == "recovered"
    assert result["final_status"] == GradeFinalStatus.APPROVED


def test_s2_two_failed_learning_outcomes_fail_without_recovery():
    result = calculate_s2_grade([_outcome(29), _outcome(20), _outcome(45)])

    assert result["final_status"] == GradeFinalStatus.FAILED
    assert result["failed_learning_outcomes_count"] == 2
    assert result["recovery_required"] is False
