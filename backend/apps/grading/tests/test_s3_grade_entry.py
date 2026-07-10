import pytest
from rest_framework.test import APIClient

from apps.grading.models import GradeCalculationSnapshot, GradeFinalStatus, GradingModel
from apps.grading.services import open_gradebook
from apps.grading.tests.factories import (
    add_s3_structure,
    make_course_enrollment,
    make_gradebook,
)
from apps.people.tests.factories import make_user


def _teacher_user(gradebook):
    user = make_user("docente-s3@example.edu", "USR-S3", "Docente")
    person = gradebook.syllabus.lead_teacher.person
    person.user = user
    person.save()
    return user


@pytest.mark.django_db
def test_s3_partial_entry_calculates_three_partials_and_requires_final_evaluation():
    gradebook = make_gradebook(code="S7T3A", grading_model=GradingModel.S3)
    open_gradebook(gradebook)
    structure = add_s3_structure(gradebook)
    course_enrollment = make_course_enrollment(
        code="S7T3A",
        course_section=gradebook.course_section,
    )
    user = _teacher_user(gradebook)
    client = APIClient()
    client.force_authenticate(user)

    for partial in structure["partials"]:
        response = client.post(
            f"/api/grading/teacher/gradebooks/{gradebook.id}/s3-partial-entry/",
            {
                "partial": partial["partial"].id,
                "entries": [
                    {
                        "course_enrollment": course_enrollment.id,
                        "practice_scores": {str(partial["practice"].id): "20"},
                        "evaluation_score": "20",
                    }
                ],
            },
            format="json",
        )
        assert response.status_code == 200

    snapshot = GradeCalculationSnapshot.objects.get(is_current=True)
    assert snapshot.final_status == GradeFinalStatus.RECOVERY_REQUIRED
    assert snapshot.recovery_required is True
    assert len(snapshot.payload["partials"]) == 3


@pytest.mark.django_db
def test_s3_final_evaluation_updates_final_status():
    gradebook = make_gradebook(code="S7T3B", grading_model=GradingModel.S3)
    open_gradebook(gradebook)
    structure = add_s3_structure(gradebook)
    course_enrollment = make_course_enrollment(
        code="S7T3B",
        course_section=gradebook.course_section,
    )
    user = _teacher_user(gradebook)
    client = APIClient()
    client.force_authenticate(user)

    for partial in structure["partials"]:
        client.post(
            f"/api/grading/teacher/gradebooks/{gradebook.id}/s3-partial-entry/",
            {
                "partial": partial["partial"].id,
                "entries": [
                    {
                        "course_enrollment": course_enrollment.id,
                        "practice_scores": {str(partial["practice"].id): "20"},
                        "evaluation_score": "20",
                    }
                ],
            },
            format="json",
        )
    response = client.post(
        f"/api/grading/teacher/gradebooks/{gradebook.id}/s3-final-evaluation/",
        {
            "final_evaluation": structure["final_evaluation"].id,
            "entries": [{"course_enrollment": course_enrollment.id, "score": "35"}],
        },
        format="json",
    )

    assert response.status_code == 200
    snapshot = GradeCalculationSnapshot.objects.get(is_current=True)
    assert snapshot.final_status == GradeFinalStatus.APPROVED
    assert str(snapshot.final_score) == "30.00"
