import pytest

from apps.grading.models import GradeFinalStatus, GradingModel
from apps.grading.services import (
    close_gradebook,
    open_gradebook,
    recalculate_gradebook,
    save_grade_record,
)
from apps.grading.tests.factories import (
    add_s1_s2_structure,
    add_s3_structure,
    make_course_enrollment,
    make_gradebook,
)
from apps.people.tests.factories import make_user


def _save_scores(gradebook, course_enrollment, item_scores, user):
    for item, score in item_scores:
        save_grade_record(
            gradebook=gradebook,
            course_enrollment=course_enrollment,
            grade_item=item,
            score=score,
            user=user,
        )


@pytest.mark.django_db
def test_acceptance_s1_complete_flow_closes_approved_gradebook():
    user = make_user("docente-s8qa-s1@example.edu", "USR-S8QA-S1", "Docente")
    gradebook = make_gradebook(code="S8QA-S1", grading_model=GradingModel.S1)
    open_gradebook(gradebook, user=user)
    items = add_s1_s2_structure(gradebook)
    course_enrollment = make_course_enrollment(
        code="S8QA-S1",
        course_section=gradebook.course_section,
    )

    _save_scores(
        gradebook,
        course_enrollment,
        [(item["activity"], 35) for item in items],
        user,
    )
    snapshot = recalculate_gradebook(
        gradebook,
        course_enrollments=[course_enrollment],
        user=user,
    )[0]
    close_gradebook(gradebook, user=user)

    gradebook.refresh_from_db()
    assert snapshot.final_status == GradeFinalStatus.APPROVED
    assert snapshot.final_score == 35
    assert gradebook.status == "closed"


@pytest.mark.django_db
def test_acceptance_s2_one_failed_outcome_recovers_and_closes():
    user = make_user("docente-s8qa-s2@example.edu", "USR-S8QA-S2", "Docente")
    gradebook = make_gradebook(code="S8QA-S2", grading_model=GradingModel.S2)
    open_gradebook(gradebook, user=user)
    items = add_s1_s2_structure(gradebook)
    course_enrollment = make_course_enrollment(
        code="S8QA-S2",
        course_section=gradebook.course_section,
    )

    _save_scores(
        gradebook,
        course_enrollment,
        [
            (items[0]["activity"], 25),
            (items[0]["recovery"], 35),
            (items[1]["activity"], 40),
            (items[2]["activity"], 42),
        ],
        user,
    )
    snapshot = recalculate_gradebook(
        gradebook,
        course_enrollments=[course_enrollment],
        user=user,
    )[0]
    close_gradebook(gradebook, user=user)

    assert snapshot.final_status == GradeFinalStatus.APPROVED
    assert snapshot.payload["learning_outcomes"][0]["final_score"] == "30.00"
    assert snapshot.recovery_required is False


@pytest.mark.django_db
def test_acceptance_s3_final_evaluation_recovers_and_closes():
    user = make_user("docente-s8qa-s3@example.edu", "USR-S8QA-S3", "Docente")
    gradebook = make_gradebook(code="S8QA-S3", grading_model=GradingModel.S3)
    open_gradebook(gradebook, user=user)
    structure = add_s3_structure(gradebook)
    course_enrollment = make_course_enrollment(
        code="S8QA-S3",
        course_section=gradebook.course_section,
    )

    scores = []
    for partial in structure["partials"]:
        scores.extend(
            [
                (partial["practice"], 25),
                (partial["evaluation"], 25),
            ]
        )
    scores.append((structure["final_evaluation"], 38))
    _save_scores(gradebook, course_enrollment, scores, user)
    snapshot = recalculate_gradebook(
        gradebook,
        course_enrollments=[course_enrollment],
        user=user,
    )[0]
    close_gradebook(gradebook, user=user)

    assert snapshot.final_status == GradeFinalStatus.APPROVED
    assert snapshot.final_score == 30
    assert snapshot.payload["preliminary_score"] == "25.00"
