import pytest
from rest_framework.test import APIClient

from apps.academic_catalogs.tests.factories import make_career
from apps.people.tests.factories import make_person, make_student, make_user


@pytest.mark.django_db
def test_secretary_can_create_student():
    user = make_user(
        "secretaria-estudiantes@example.edu",
        "USR-STUDENT-001",
        "Secretaria",
    )
    person = make_person("ID-API-STUDENT-001")
    career = make_career("CAR-API-ST-001")
    client = APIClient()
    client.force_authenticate(user)

    response = client.post(
        "/api/students/",
        {
            "person": person.id,
            "student_code": "EST-API-001",
            "career": career.id,
            "status": "activo",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["student_code"] == "EST-API-001"


@pytest.mark.django_db
def test_student_can_read_only_own_profile():
    user = make_user("estudiante-api@example.edu", "USR-STUDENT-002", "Estudiante")
    own_person = make_person("ID-API-STUDENT-002", user=user)
    own_student = make_student(person=own_person, student_code="EST-API-002")
    make_student(student_code="EST-API-003")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/students/")

    assert response.status_code == 200
    assert [student["id"] for student in response.data] == [own_student.id]


@pytest.mark.django_db
def test_teacher_cannot_read_students_without_course_scope():
    user = make_user("docente-estudiantes@example.edu", "USR-STUDENT-003", "Docente")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/students/")

    assert response.status_code == 403
