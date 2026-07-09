import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from apps.audit.models import AuditLog
from apps.grading.models import GradebookStatus, GradingModel
from apps.grading.services import (
    close_gradebook,
    delete_grade_record,
    reopen_gradebook,
    save_grade_record,
)
from apps.grading.tests.factories import (
    add_s1_s2_structure,
    make_course_enrollment,
    make_gradebook,
)


def _user():
    return get_user_model().objects.create_user(
        email="docente.notas@example.edu",
        password="test-pass",
        names="Docente",
        last_names="Sintetico",
        identification="DOC-NOTAS",
    )


@pytest.mark.django_db
def test_grade_record_changes_are_audited():
    user = _user()
    gradebook = make_gradebook(code="AUD1", grading_model=GradingModel.S1)
    course_enrollment = make_course_enrollment(
        code="AUD1",
        course_section=gradebook.course_section,
    )
    item = add_s1_s2_structure(gradebook)[0]["activity"]

    record = save_grade_record(
        gradebook=gradebook,
        course_enrollment=course_enrollment,
        grade_item=item,
        score=40,
        user=user,
    )
    save_grade_record(
        gradebook=gradebook,
        course_enrollment=course_enrollment,
        grade_item=item,
        score=42,
        user=user,
        reason="Ajuste sintetico",
    )
    delete_grade_record(record, user=user, reason="Anulacion sintetica")

    assert AuditLog.objects.filter(action="grade_record_created").exists()
    assert AuditLog.objects.filter(action="grade_record_updated").exists()
    assert AuditLog.objects.filter(action="grade_record_deleted").exists()


@pytest.mark.django_db
def test_closed_gradebook_blocks_normal_changes_and_reopen_requires_reason():
    user = _user()
    gradebook = make_gradebook(code="AUD2", grading_model=GradingModel.S1)
    course_enrollment = make_course_enrollment(
        code="AUD2",
        course_section=gradebook.course_section,
    )
    item = add_s1_s2_structure(gradebook)[0]["activity"]
    close_gradebook(gradebook, user=user)

    with pytest.raises(ValidationError):
        save_grade_record(
            gradebook=gradebook,
            course_enrollment=course_enrollment,
            grade_item=item,
            score=40,
            user=user,
        )

    with pytest.raises(ValidationError):
        reopen_gradebook(gradebook, reason="", user=user)

    reopen_gradebook(gradebook, reason="Correccion autorizada sintetica", user=user)
    gradebook.refresh_from_db()

    assert gradebook.status == GradebookStatus.REOPENED
    assert AuditLog.objects.filter(action="gradebook_reopened").exists()
