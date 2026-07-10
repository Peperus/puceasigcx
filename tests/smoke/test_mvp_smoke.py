import pytest
from rest_framework.test import APIClient

from apps.people.tests.factories import make_user


@pytest.mark.django_db
def test_smoke_public_health_and_version_endpoints():
    client = APIClient()

    health = client.get("/api/health/")
    version = client.get("/api/version/")

    assert health.status_code == 200
    assert health.data["status"] == "ok"
    assert version.status_code == 200
    assert version.data["service"]


@pytest.mark.django_db
def test_smoke_protected_report_requires_authentication():
    client = APIClient()

    response = client.get("/api/reports/mvp/students/")

    assert response.status_code == 401


@pytest.mark.django_db
def test_smoke_authorized_secretary_can_open_empty_mvp_report():
    user = make_user("secretaria-smoke@example.edu", "USR-SMOKE", "Secretaria")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/reports/mvp/students/")

    assert response.status_code == 200
    assert response.data["report_type"] == "students"
    assert response.data["count"] == 0
