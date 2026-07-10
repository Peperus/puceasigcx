import pytest
from rest_framework.test import APIClient

from apps.audit.models import AuditLog
from apps.grading.models import GradeCalculationSnapshot, GradeFinalStatus, GradingModel
from apps.grading.services import open_gradebook
from apps.grading.tests.factories import (
    add_s1_s2_structure,
    make_course_enrollment,
    make_gradebook,
)
from apps.people.tests.factories import make_user


def _teacher_user(gradebook, suffix="T1"):
    user = make_user(
        f"docente-{suffix}@example.edu",
        f"USR-{suffix}",
        "Docente",
    )
    person = gradebook.syllabus.lead_teacher.person
    person.user = user
    person.save()
    return user


@pytest.mark.django_db
def test_teacher_lists_only_assigned_gradebooks_and_students():
    gradebook = make_gradebook(code="S7T1A", grading_model=GradingModel.S1)
    add_s1_s2_structure(gradebook)
    course_enrollment = make_course_enrollment(
        code="S7T1A",
        course_section=gradebook.course_section,
    )
    other_gradebook = make_gradebook(code="S7T1B", grading_model=GradingModel.S1)
    add_s1_s2_structure(other_gradebook)
    user = _teacher_user(gradebook)
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/grading/teacher/gradebooks/")
    students_response = client.get(
        f"/api/grading/teacher/gradebooks/{gradebook.id}/students/"
    )

    assert response.status_code == 200
    assert [row["id"] for row in response.data] == [gradebook.id]
    assert other_gradebook.id not in [row["id"] for row in response.data]
    assert students_response.status_code == 200
    assert students_response.data[0]["id"] == course_enrollment.id


@pytest.mark.django_db
def test_teacher_cannot_edit_other_course_or_closed_gradebook():
    gradebook = make_gradebook(code="S7T1C", grading_model=GradingModel.S1)
    items = add_s1_s2_structure(gradebook)
    course_enrollment = make_course_enrollment(
        code="S7T1C",
        course_section=gradebook.course_section,
    )
    other_gradebook = make_gradebook(code="S7T1D", grading_model=GradingModel.S1)
    _teacher_user(other_gradebook, "T1D")
    user = _teacher_user(gradebook, "T1C")
    client = APIClient()
    client.force_authenticate(user)

    closed_response = client.post(
        f"/api/grading/teacher/gradebooks/{gradebook.id}/record/",
        {
            "course_enrollment": course_enrollment.id,
            "grade_item": items[0]["activity"].id,
            "score": "40",
        },
        format="json",
    )
    other_response = client.post(
        f"/api/grading/teacher/gradebooks/{other_gradebook.id}/record/",
        {
            "course_enrollment": course_enrollment.id,
            "grade_item": items[0]["activity"].id,
            "score": "40",
        },
        format="json",
    )

    assert closed_response.status_code == 400
    assert other_response.status_code == 404


@pytest.mark.django_db
def test_teacher_grade_entry_rejects_out_of_range_and_audits_valid_save():
    gradebook = make_gradebook(code="S7T1E", grading_model=GradingModel.S1)
    open_gradebook(gradebook)
    items = add_s1_s2_structure(gradebook)
    course_enrollment = make_course_enrollment(
        code="S7T1E",
        course_section=gradebook.course_section,
    )
    user = _teacher_user(gradebook, "T1E")
    client = APIClient()
    client.force_authenticate(user)

    bad_response = client.post(
        f"/api/grading/teacher/gradebooks/{gradebook.id}/record/",
        {
            "course_enrollment": course_enrollment.id,
            "grade_item": items[0]["activity"].id,
            "score": "51",
        },
        format="json",
    )
    valid_response = client.post(
        f"/api/grading/teacher/gradebooks/{gradebook.id}/record/",
        {
            "course_enrollment": course_enrollment.id,
            "grade_item": items[0]["activity"].id,
            "score": "40",
        },
        format="json",
    )

    assert bad_response.status_code == 400
    assert valid_response.status_code == 200
    assert AuditLog.objects.filter(action="grade_record_created").exists()
    snapshot = GradeCalculationSnapshot.objects.get(is_current=True)
    assert snapshot.final_status == GradeFinalStatus.PENDING
