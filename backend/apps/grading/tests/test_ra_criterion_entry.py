import pytest
from rest_framework.test import APIClient

from apps.grading.models import GradeCalculationSnapshot, GradeFinalStatus, GradingModel
from apps.grading.services import open_gradebook
from apps.grading.tests.factories import (
    add_s1_s2_structure,
    make_course_enrollment,
    make_gradebook,
)
from apps.people.tests.factories import make_user


def _teacher_user(gradebook):
    user = make_user("docente-ra@example.edu", "USR-RA", "Docente")
    person = gradebook.syllabus.lead_teacher.person
    person.user = user
    person.save()
    return user


@pytest.mark.django_db
def test_ra_criterion_bulk_entry_is_transactional_and_reports_row_errors():
    gradebook = make_gradebook(code="S7T2A", grading_model=GradingModel.S1)
    open_gradebook(gradebook)
    items = add_s1_s2_structure(gradebook)
    course_enrollment = make_course_enrollment(
        code="S7T2A",
        course_section=gradebook.course_section,
    )
    user = _teacher_user(gradebook)
    client = APIClient()
    client.force_authenticate(user)

    response = client.post(
        f"/api/grading/teacher/gradebooks/{gradebook.id}/ra-criterion-entry/",
        {
            "learning_outcome": items[0]["outcome"].id,
            "criterion": items[0]["criterion"].id,
            "entries": [
                {"course_enrollment": course_enrollment.id, "score": "42"},
                {"course_enrollment": 999999, "score": "40"},
            ],
        },
        format="json",
    )

    assert response.status_code == 400
    assert "entries" in response.data
    assert GradeCalculationSnapshot.objects.count() == 0


@pytest.mark.django_db
def test_ra_criterion_bulk_entry_updates_summary_with_letters():
    gradebook = make_gradebook(code="S7T2B", grading_model=GradingModel.S1)
    open_gradebook(gradebook)
    items = add_s1_s2_structure(gradebook)
    course_enrollment = make_course_enrollment(
        code="S7T2B",
        course_section=gradebook.course_section,
    )
    user = _teacher_user(gradebook)
    client = APIClient()
    client.force_authenticate(user)

    for item in items:
        response = client.post(
            f"/api/grading/teacher/gradebooks/{gradebook.id}/ra-criterion-entry/",
            {
                "learning_outcome": item["outcome"].id,
                "criterion": item["criterion"].id,
                "entries": [{"course_enrollment": course_enrollment.id, "score": "45"}],
            },
            format="json",
        )
        assert response.status_code == 200

    snapshot = GradeCalculationSnapshot.objects.get(is_current=True)
    assert snapshot.final_status == GradeFinalStatus.APPROVED
    assert snapshot.final_letter == "A"
    assert snapshot.payload["learning_outcomes"][0]["letter"] == "A"
