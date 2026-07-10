import pytest
from rest_framework.test import APIClient

from apps.audit.models import AuditLog
from apps.grading.models import GradebookStatus, GradingModel
from apps.grading.services import open_gradebook, save_grade_record
from apps.grading.tests.factories import (
    add_s1_s2_structure,
    make_course_enrollment,
    make_gradebook,
)
from apps.people.tests.factories import make_user


@pytest.mark.django_db
def test_gradebook_close_rejects_incomplete_grades():
    gradebook = make_gradebook(code="S7T6A", grading_model=GradingModel.S1)
    open_gradebook(gradebook)
    add_s1_s2_structure(gradebook)
    make_course_enrollment(code="S7T6A", course_section=gradebook.course_section)
    user = make_user("secretaria-s7t6@example.edu", "USR-S7T6", "Secretaria")
    client = APIClient()
    client.force_authenticate(user)

    response = client.post(f"/api/grading/gradebooks/{gradebook.id}/close/")

    assert response.status_code == 400
    gradebook.refresh_from_db()
    assert gradebook.status != GradebookStatus.CLOSED


@pytest.mark.django_db
def test_gradebook_close_generates_final_snapshot_and_blocks_teacher_edit():
    gradebook = make_gradebook(code="S7T6B", grading_model=GradingModel.S1)
    open_gradebook(gradebook)
    items = add_s1_s2_structure(gradebook)
    course_enrollment = make_course_enrollment(
        code="S7T6B",
        course_section=gradebook.course_section,
    )
    for item in items:
        save_grade_record(
            gradebook=gradebook,
            course_enrollment=course_enrollment,
            grade_item=item["activity"],
            score=40,
        )
    secretary = make_user(
        "secretaria-s7t6b@example.edu",
        "USR-S7T6B",
        "Secretaria",
    )
    teacher = make_user("docente-s7t6b@example.edu", "USR-S7T6BT", "Docente")
    person = gradebook.syllabus.lead_teacher.person
    person.user = teacher
    person.save()
    client = APIClient()
    client.force_authenticate(secretary)

    close_response = client.post(f"/api/grading/gradebooks/{gradebook.id}/close/")
    client.force_authenticate(teacher)
    edit_response = client.post(
        f"/api/grading/teacher/gradebooks/{gradebook.id}/record/",
        {
            "course_enrollment": course_enrollment.id,
            "grade_item": items[0]["activity"].id,
            "score": "41",
        },
        format="json",
    )

    assert close_response.status_code == 200
    assert close_response.data["status"] == GradebookStatus.CLOSED
    assert AuditLog.objects.filter(action="gradebook_closed").exists()
    assert gradebook.calculation_snapshots.filter(
        is_current=True,
        source="gradebook_closure",
    ).exists()
    assert edit_response.status_code == 400


@pytest.mark.django_db
def test_gradebook_reopen_requires_reason_and_authorized_role():
    gradebook = make_gradebook(code="S7T6C", grading_model=GradingModel.S1)
    open_gradebook(gradebook)
    items = add_s1_s2_structure(gradebook)
    course_enrollment = make_course_enrollment(
        code="S7T6C",
        course_section=gradebook.course_section,
    )
    for item in items:
        save_grade_record(
            gradebook=gradebook,
            course_enrollment=course_enrollment,
            grade_item=item["activity"],
            score=40,
        )
    user = make_user("secretaria-s7t6c@example.edu", "USR-S7T6C", "Secretaria")
    client = APIClient()
    client.force_authenticate(user)
    client.post(f"/api/grading/gradebooks/{gradebook.id}/close/")

    bad_response = client.post(f"/api/grading/gradebooks/{gradebook.id}/reopen/")
    ok_response = client.post(
        f"/api/grading/gradebooks/{gradebook.id}/reopen/",
        {"reason": "Correccion autorizada sintetica"},
        format="json",
    )

    assert bad_response.status_code == 400
    assert ok_response.status_code == 200
    assert ok_response.data["status"] == GradebookStatus.REOPENED
    assert AuditLog.objects.filter(action="gradebook_reopened").exists()
