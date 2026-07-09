import pytest
from rest_framework.test import APIClient

from apps.academic_catalogs.tests.factories import make_domain
from apps.people.tests.factories import make_person, make_teacher, make_user


@pytest.mark.django_db
def test_secretary_can_create_teacher():
    user = make_user(
        "secretaria-docentes@example.edu",
        "USR-TEACHER-001",
        "Secretaria",
    )
    person = make_person("ID-API-TEACHER-001")
    domain = make_domain("DOM-API-TEACH-001")
    client = APIClient()
    client.force_authenticate(user)

    response = client.post(
        "/api/teachers/",
        {
            "person": person.id,
            "teacher_code": "DOC-API-001",
            "academic_degree": "Mgtr.",
            "professional_title": "Titulo sintetico",
            "academic_profile": "Perfil sintetico",
            "status": "activo",
            "domains": [domain.id],
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["teacher_code"] == "DOC-API-001"


@pytest.mark.django_db
def test_teacher_can_read_only_own_profile():
    user = make_user("docente-api@example.edu", "USR-TEACHER-002", "Docente")
    own_person = make_person("ID-API-TEACHER-002", user=user)
    own_teacher = make_teacher(person=own_person, teacher_code="DOC-API-002")
    make_teacher(teacher_code="DOC-API-003")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/teachers/")

    assert response.status_code == 200
    assert [teacher["id"] for teacher in response.data] == [own_teacher.id]


@pytest.mark.django_db
def test_student_cannot_read_teachers_endpoint():
    user = make_user("estudiante-docentes@example.edu", "USR-TEACHER-003", "Estudiante")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/teachers/")

    assert response.status_code == 403
