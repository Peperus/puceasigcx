import zipfile
from io import BytesIO

import pytest
from rest_framework.test import APIClient

from apps.audit.models import AuditLog
from apps.enrollment.models import TeachingAssignment, TeachingRole
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
from apps.people.tests.factories import make_teacher, make_user


def _graded_course(code="S8RPT"):
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
            score=42,
        )
    recalculate_gradebook(gradebook, course_enrollments=[course_enrollment])
    return gradebook, course_enrollment


@pytest.mark.django_db
def test_mvp_reports_filter_students_by_period_and_career():
    gradebook, course_enrollment = _graded_course()
    user = make_user("secretaria-s8t1@example.edu", "USR-S8T1", "Secretaria")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get(
        "/api/reports/mvp/students/",
        {
            "period": gradebook.course_section.offer.period.code,
            "career": gradebook.course_section.offer.career.id,
        },
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["student_code"] == (
        course_enrollment.enrollment.student.student_code
    )


@pytest.mark.django_db
def test_mvp_teacher_course_syllabus_and_grade_reports_return_expected_rows():
    gradebook, _course_enrollment = _graded_course("S8RPT2")
    extra_teacher = make_teacher(teacher_code="DOC-S8RPT2B")
    TeachingAssignment.objects.create(
        course_section=gradebook.course_section,
        teacher=extra_teacher,
        role=TeachingRole.CO_TEACHER,
    )
    user = make_user("coord-s8t1@example.edu", "USR-S8T1C", "Coordinador de carrera")
    career = gradebook.course_section.offer.career
    career.coordinator_user = user
    career.save()
    client = APIClient()
    client.force_authenticate(user)

    teachers = client.get("/api/reports/mvp/teachers/", {"career": career.id})
    courses = client.get("/api/reports/mvp/courses/", {"career": career.id})
    syllabi = client.get("/api/reports/mvp/syllabi/", {"career": career.id})
    grades = client.get("/api/reports/mvp/grades/", {"career": career.id})

    assert teachers.status_code == 200
    assert teachers.data["count"] == 2
    assert courses.status_code == 200
    assert courses.data["results"][0]["subject_code"] == (
        gradebook.course_section.subject.code
    )
    assert syllabi.status_code == 200
    assert syllabi.data["results"][0]["status"] == gradebook.syllabus.status
    assert grades.status_code == 200
    assert grades.data["results"][0]["grading_model"] == GradingModel.S1


@pytest.mark.django_db
def test_mvp_report_export_csv_and_xlsx_audits_download():
    gradebook, _course_enrollment = _graded_course("S8RPT3")
    user = make_user("secretaria-s8t1x@example.edu", "USR-S8T1X", "Secretaria")
    client = APIClient()
    client.force_authenticate(user)

    csv_response = client.get(
        "/api/reports/mvp/courses/",
        {"career": gradebook.course_section.offer.career.id, "file_format": "csv"},
    )
    xlsx_response = client.get(
        "/api/reports/mvp/courses/",
        {"career": gradebook.course_section.offer.career.id, "file_format": "xlsx"},
    )

    assert csv_response.status_code == 200
    assert csv_response["Content-Type"].startswith("text/csv")
    assert gradebook.course_section.subject.code in csv_response.content.decode()
    assert xlsx_response.status_code == 200
    with zipfile.ZipFile(BytesIO(xlsx_response.content)) as workbook:
        assert "xl/worksheets/sheet1.xml" in workbook.namelist()
    assert (
        AuditLog.objects.filter(
            action="mvp_report_exported",
            object_id="cursos-activos-mvp",
        ).count()
        == 2
    )


@pytest.mark.django_db
def test_mvp_reports_reject_student_role():
    _graded_course("S8RPT4")
    user = make_user("estudiante-s8t1@example.edu", "USR-S8T1S", "Estudiante")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/reports/mvp/students/")

    assert response.status_code == 403
