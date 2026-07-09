import pytest
from rest_framework.test import APIClient

from apps.people.tests.factories import make_user
from apps.syllabus.tests.factories import make_complete_syllabus


@pytest.mark.django_db
def test_syllabus_printable_endpoint_includes_required_sections():
    secretary = make_user("secretaria-s5t8@example.edu", "USR-S5T8SEC", "Secretaria")
    syllabus = make_complete_syllabus("S5T8")
    client = APIClient()
    client.force_authenticate(secretary)

    response = client.get(f"/api/syllabi/{syllabus.id}/printable/")
    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "Datos informativos" in content
    assert "Resultados y rubricas" in content
    assert "Planificacion semanal" in content
    assert "Bibliografia" in content
    assert syllabus.course_section.subject.name in content
