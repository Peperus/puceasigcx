import pytest
from rest_framework.test import APIClient

from apps.audit.models import AuditLog
from apps.enrollment.services import save_course_enrollment
from apps.grading.models import GradingModel
from apps.grading.services import close_gradebook, open_gradebook, save_grade_record
from apps.grading.tests.factories import (
    add_s1_s2_structure,
    make_course_enrollment,
    make_gradebook,
)
from apps.people.tests.factories import make_user
from apps.syllabus.models import SyllabusStatus
from apps.syllabus.services import approve_syllabus, finalize_syllabus, submit_syllabus
from apps.syllabus.tests.factories import make_complete_syllabus


@pytest.mark.django_db
def test_cross_module_audit_logs_critical_actions():
    secretary = make_user("secretaria-s8t2@example.edu", "USR-S8T2", "Secretaria")
    course_enrollment = make_course_enrollment(code="S8AUD")

    save_course_enrollment(course_enrollment, user=secretary)

    syllabus = make_complete_syllabus("S8AUDS")
    finalize_syllabus(syllabus, user=secretary)
    submit_syllabus(syllabus, user=secretary)
    approve_syllabus(syllabus, user=secretary)

    gradebook = make_gradebook(code="S8AUDG", grading_model=GradingModel.S1)
    open_gradebook(gradebook, user=secretary)
    items = add_s1_s2_structure(gradebook)
    enrolled = make_course_enrollment(
        code="S8AUDG",
        course_section=gradebook.course_section,
    )
    save_grade_record(
        gradebook=gradebook,
        course_enrollment=enrolled,
        grade_item=items[0]["activity"],
        score=38,
        user=secretary,
    )
    close_gradebook(gradebook, user=secretary, allow_incomplete=True)

    assert AuditLog.objects.filter(action="course_enrollment_updated").exists()
    assert AuditLog.objects.filter(
        action="syllabus_approved",
        new_data__status=SyllabusStatus.APPROVED,
    ).exists()
    assert AuditLog.objects.filter(action="grade_record_created").exists()
    assert AuditLog.objects.filter(action="gradebook_closed").exists()


@pytest.mark.django_db
def test_audit_api_is_read_only_filterable_and_role_protected():
    secretary = make_user("secretaria-audit-api@example.edu", "USR-S8T2A", "Secretaria")
    teacher = make_user("docente-audit-api@example.edu", "USR-S8T2B", "Docente")
    AuditLog.objects.create(
        user=secretary,
        action="grade_record_created",
        module="grading",
        model_name="StudentGradeRecord",
        object_id="123",
        new_data={"score": "40.00"},
    )
    client = APIClient()
    client.force_authenticate(secretary)

    list_response = client.get("/api/audit/logs/", {"module": "grading"})
    create_response = client.post(
        "/api/audit/logs/",
        {"action": "manual"},
        format="json",
    )
    client.force_authenticate(teacher)
    forbidden_response = client.get("/api/audit/logs/")

    assert list_response.status_code == 200
    assert list_response.data[0]["action"] == "grade_record_created"
    assert create_response.status_code == 405
    assert forbidden_response.status_code == 403
