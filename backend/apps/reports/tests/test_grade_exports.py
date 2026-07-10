import zipfile
from io import BytesIO

import pytest
from rest_framework.test import APIClient

from apps.audit.models import AuditLog
from apps.grading.models import GradingModel
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


def _snapshot():
    gradebook = make_gradebook(code="S7T7", grading_model=GradingModel.S1)
    open_gradebook(gradebook)
    items = add_s1_s2_structure(gradebook)
    course_enrollment = make_course_enrollment(
        code="S7T7",
        course_section=gradebook.course_section,
    )
    for item in items:
        save_grade_record(
            gradebook=gradebook,
            course_enrollment=course_enrollment,
            grade_item=item["activity"],
            score=45,
        )
    return recalculate_gradebook(gradebook, course_enrollments=[course_enrollment])[0]


@pytest.mark.django_db
def test_grade_export_csv_downloads_valid_file_and_audits():
    snapshot = _snapshot()
    user = make_user("secretaria-s7t7@example.edu", "USR-S7T7", "Secretaria")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get(
        "/api/reports/grades/export/",
        {"gradebook": snapshot.gradebook_id, "file_format": "csv"},
    )

    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/csv")
    assert "attachment" in response["Content-Disposition"]
    assert "SUB-S7T7" in response.content.decode()
    assert AuditLog.objects.filter(action="grade_report_exported").exists()


@pytest.mark.django_db
def test_grade_export_xlsx_downloads_zip_package():
    snapshot = _snapshot()
    user = make_user("secretaria-s7t7x@example.edu", "USR-S7T7X", "Secretaria")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get(
        "/api/reports/grades/export/",
        {"gradebook": snapshot.gradebook_id, "file_format": "xlsx"},
    )

    assert response.status_code == 200
    with zipfile.ZipFile(BytesIO(response.content)) as workbook:
        assert "xl/worksheets/sheet1.xml" in workbook.namelist()


@pytest.mark.django_db
def test_grade_export_rejects_student_role():
    _snapshot()
    user = make_user("estudiante-s7t7@example.edu", "USR-S7T7S", "Estudiante")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/reports/grades/export/")

    assert response.status_code == 403
