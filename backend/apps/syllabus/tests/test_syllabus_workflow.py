import pytest
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient

from apps.audit.models import AuditLog
from apps.people.tests.factories import make_user
from apps.syllabus.models import SyllabusStatus
from apps.syllabus.services import (
    approve_syllabus,
    finalize_syllabus,
    is_syllabus_ready_for_grading,
    observe_syllabus,
    reopen_syllabus,
    submit_syllabus,
)
from apps.syllabus.tests.factories import make_complete_syllabus


@pytest.mark.django_db
def test_syllabus_workflow_finalizes_submits_and_approves_with_audit():
    coordinator = make_user(
        "coord-s5t6@example.edu",
        "USR-S5T6CO",
        "Coordinador de carrera",
    )
    syllabus = make_complete_syllabus("S5T6")
    syllabus.course_section.offer.career.coordinator_user = coordinator
    syllabus.course_section.offer.career.save()

    finalize_syllabus(syllabus)
    submit_syllabus(syllabus)
    approve_syllabus(syllabus, user=coordinator)

    syllabus.refresh_from_db()
    assert syllabus.status == SyllabusStatus.APPROVED
    assert syllabus.approved_by == coordinator
    assert is_syllabus_ready_for_grading(syllabus.course_section)
    assert AuditLog.objects.filter(module="syllabus").count() == 3


@pytest.mark.django_db
def test_assigned_teacher_cannot_approve_own_syllabus():
    teacher_user = make_user("docente-s5t6@example.edu", "USR-S5T6TE", "Docente")
    syllabus = make_complete_syllabus("S5T6SELF", user=teacher_user)
    finalize_syllabus(syllabus, user=teacher_user)
    submit_syllabus(syllabus, user=teacher_user)

    with pytest.raises(ValidationError) as exc:
        approve_syllabus(syllabus, user=teacher_user)

    assert "propio silabo" in str(exc.value.message_dict)


@pytest.mark.django_db
def test_reviewer_can_observe_and_reopen_with_reason():
    secretary = make_user("secretaria-s5t6@example.edu", "USR-S5T6SEC", "Secretaria")
    syllabus = make_complete_syllabus("S5T6OBS")
    finalize_syllabus(syllabus)
    submit_syllabus(syllabus)

    observe_syllabus(syllabus, reason="Ajustar bibliografia.", user=secretary)
    syllabus.refresh_from_db()
    assert syllabus.status == SyllabusStatus.OBSERVED

    reopen_syllabus(syllabus, reason="Correccion autorizada.", user=secretary)
    syllabus.refresh_from_db()
    assert syllabus.status == SyllabusStatus.DRAFT


@pytest.mark.django_db
def test_teacher_can_finalize_and_submit_from_api():
    teacher_user = make_user("docente-api-s5t6@example.edu", "USR-S5T6API", "Docente")
    syllabus = make_complete_syllabus("S5T6API", user=teacher_user)
    client = APIClient()
    client.force_authenticate(teacher_user)

    finalize_response = client.post(f"/api/syllabi/{syllabus.id}/finalize/")
    submit_response = client.post(f"/api/syllabi/{syllabus.id}/submit/")

    assert finalize_response.status_code == 200
    assert submit_response.status_code == 200
    assert submit_response.data["status"] == SyllabusStatus.IN_REVIEW
