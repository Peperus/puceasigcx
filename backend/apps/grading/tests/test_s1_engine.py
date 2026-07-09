from apps.grading.models import GradeFinalStatus
from apps.grading.services import calculate_s1_grade


def _outcome(score, recovery_score=None):
    data = {"criteria": [{"weight": 100, "score": score}]}
    if recovery_score is not None:
        data["recovery_score"] = recovery_score
    return data


def test_s1_approves_only_when_all_learning_outcomes_pass():
    result = calculate_s1_grade([_outcome(30), _outcome(40), _outcome(45)])

    assert result["final_status"] == GradeFinalStatus.APPROVED
    assert result["failed_learning_outcomes_count"] == 0
    assert result["final_letter"] == "C"


def test_s1_failed_learning_outcome_keeps_course_not_approved():
    result = calculate_s1_grade([_outcome(29), _outcome(40), _outcome(45)])

    assert result["final_status"] == GradeFinalStatus.INTERSEMESTRAL
    assert result["failed_learning_outcomes_count"] == 1
    assert result["recovery_required"] is True


def test_s1_recovery_can_reach_minimum_but_not_exceed_cap():
    result = calculate_s1_grade([_outcome(29, 50), _outcome(40), _outcome(45)])
    recovered = result["learning_outcomes"][0]

    assert recovered["final_score"] == 30
    assert recovered["status"] == "recovered"
    assert result["final_status"] == GradeFinalStatus.APPROVED
