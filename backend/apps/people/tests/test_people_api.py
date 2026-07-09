import pytest
from rest_framework.test import APIClient

from apps.people.models import Person
from apps.people.tests.factories import make_person, make_user


@pytest.mark.django_db
def test_people_api_requires_authentication():
    response = APIClient().get("/api/people/")

    assert response.status_code == 401


@pytest.mark.django_db
def test_secretary_can_create_person():
    user = make_user(
        "secretaria-personas@example.edu",
        "USR-PEOPLE-001",
        "Secretaria",
    )
    client = APIClient()
    client.force_authenticate(user)

    response = client.post(
        "/api/people/",
        {
            "identification_number": "ID-API-PEOPLE-001",
            "first_name": "Nombre",
            "last_name": "Sintetico",
            "institutional_email": "persona-api@example.edu",
        },
        format="json",
    )

    assert response.status_code == 201
    assert Person.objects.filter(identification_number="ID-API-PEOPLE-001").exists()


@pytest.mark.django_db
def test_teacher_can_read_only_own_person():
    teacher_user = make_user(
        "docente-persona@example.edu",
        "USR-PEOPLE-002",
        "Docente",
    )
    own_person = make_person("ID-API-PEOPLE-002", user=teacher_user)
    make_person("ID-API-PEOPLE-003")
    client = APIClient()
    client.force_authenticate(teacher_user)

    response = client.get("/api/people/")

    assert response.status_code == 200
    assert [person["id"] for person in response.data] == [own_person.id]


@pytest.mark.django_db
def test_teacher_cannot_create_person():
    user = make_user("docente-personas-create@example.edu", "USR-PEOPLE-004", "Docente")
    client = APIClient()
    client.force_authenticate(user)

    response = client.post(
        "/api/people/",
        {
            "identification_number": "ID-API-PEOPLE-004",
            "first_name": "Nombre",
            "last_name": "Sintetico",
        },
        format="json",
    )

    assert response.status_code == 403
