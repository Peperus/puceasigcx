import pytest

from apps.academic_catalogs.tests.factories import make_career, make_domain
from apps.audit.models import AuditLog
from apps.people.models import Person
from apps.people.services import import_people_csv
from apps.students.models import Student
from apps.teachers.models import Teacher


@pytest.mark.django_db
def test_import_people_csv_creates_people_students_and_teachers(tmp_path):
    career = make_career("CAR-IMP-001")
    domain = make_domain("DOM-IMP-001")
    csv_path = tmp_path / "people.csv"
    csv_path.write_text(
        "\n".join(
            [
                "record_type,first_name,last_name,identification_number,"
                "institutional_email,student_code,career_code,teacher_code,"
                "academic_degree,professional_title,academic_profile,domain_codes",
                "student,Estudiante,Sintetico,IMP-001,estudiante.imp@example.edu,"
                f"EST-IMP-001,{career.code},,,,,",
                "teacher,Docente,Sintetico,IMP-002,docente.imp@example.edu,,,"
                f"DOC-IMP-001,Mgtr.,Titulo sintetico,Perfil sintetico,{domain.code}",
            ]
        ),
        encoding="utf-8",
    )

    result = import_people_csv(csv_path)

    assert result.created == 4
    assert result.rejected == 0
    assert Person.objects.count() == 2
    assert Student.objects.filter(student_code="EST-IMP-001").exists()
    teacher = Teacher.objects.get(teacher_code="DOC-IMP-001")
    assert list(teacher.domains.values_list("code", flat=True)) == [domain.code]
    assert AuditLog.objects.filter(action="people_imported").exists()


@pytest.mark.django_db
def test_import_people_csv_reports_row_errors_in_tolerant_mode(tmp_path):
    csv_path = tmp_path / "people-errors.csv"
    csv_path.write_text(
        "\n".join(
            [
                "record_type,first_name,last_name,identification_number,student_code",
                "student,Estudiante,Sintetico,IMP-ERR-001,EST-ERR-001",
            ]
        ),
        encoding="utf-8",
    )

    result = import_people_csv(csv_path)

    assert result.created == 0
    assert result.rejected == 1
    assert "career_code" in result.errors[0].message
