import pytest
from rest_framework.test import APIClient

from apps.grading.models import GradeFinalStatus, GradingModel
from apps.grading.services import (
    open_gradebook,
    recalculate_gradebook,
    save_grade_record,
)
from apps.grading.tests.factories import (
    add_s1_s2_structure,
    make_course_enrollment,
    make_gradebook,
)
from apps.people.tests.factories import make_user


def _snapshot(code, score=40):
    gradebook = make_gradebook(code=code, grading_model=GradingModel.S1)
    open_gradebook(gradebook)
    items = add_s1_s2_structure(gradebook)
    course_enrollment = make_course_enrollment(
        code=code,
        course_section=gradebook.course_section,
    )
    for item in items:
        save_grade_record(
            gradebook=gradebook,
            course_enrollment=course_enrollment,
            grade_item=item["activity"],
            score=score,
        )
    return recalculate_gradebook(
        gradebook,
        course_enrollments=[course_enrollment],
    )[0]


@pytest.mark.django_db
def test_secretary_filters_grade_queries_by_period_model_and_status():
    snapshot = _snapshot("S7T5A", score=45)
    _snapshot("S7T5B", score=20)
    user = make_user("secretaria-s7t5@example.edu", "USR-S7T5", "Secretaria")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get(
        "/api/reports/grades/",
        {
            "period": snapshot.gradebook.course_section.offer.period.code,
            "grading_model": "S1",
            "status": GradeFinalStatus.APPROVED,
        },
    )

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == snapshot.id


@pytest.mark.django_db
def test_coordinator_grade_query_is_limited_to_assigned_career():
    visible_snapshot = _snapshot("S7T5C", score=40)
    _snapshot("S7T5D", score=45)
    coordinator = make_user(
        "coord-s7t5@example.edu",
        "USR-S7T5C",
        "Coordinador de carrera",
    )
    career = visible_snapshot.gradebook.course_section.offer.career
    career.coordinator_user = coordinator
    career.save()
    client = APIClient()
    client.force_authenticate(coordinator)

    response = client.get("/api/reports/grades/")

    assert response.status_code == 200
    assert [row["id"] for row in response.data] == [visible_snapshot.id]


@pytest.mark.django_db
def test_teacher_does_not_see_massive_reports_for_unassigned_courses():
    _snapshot("S7T5E", score=40)
    teacher = make_user("docente-s7t5@example.edu", "USR-S7T5T", "Docente")
    client = APIClient()
    client.force_authenticate(teacher)

    response = client.get("/api/reports/grades/")

    assert response.status_code == 200
    assert response.data == []
