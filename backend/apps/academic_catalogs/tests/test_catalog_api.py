from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIClient

from apps.academic_catalogs.tests.factories import make_career


def make_user(email, identification, group_name=None, is_superuser=False):
    user = get_user_model().objects.create_user(
        email=email,
        password="Str0ng-pass-demo",
        names="Usuario",
        last_names="Sintetico",
        identification=identification,
        is_staff=is_superuser,
        is_superuser=is_superuser,
    )
    if group_name:
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
    return user


@pytest.mark.django_db
def test_catalog_api_requires_authentication():
    client = APIClient()

    response = client.get("/api/academic/periods/")

    assert response.status_code == 401


@pytest.mark.django_db
def test_administrator_can_create_period_from_api():
    user = make_user(
        "admin-catalogos@example.edu",
        "API-001",
        is_superuser=True,
    )
    client = APIClient()
    client.force_authenticate(user)

    response = client.post(
        "/api/academic/periods/",
        {
            "name": "Periodo API",
            "code": "API-2026",
            "start_date": date(2026, 1, 1),
            "end_date": date(2026, 6, 30),
            "enrollment_start_date": date(2026, 1, 1),
            "enrollment_end_date": date(2026, 1, 31),
            "status": "draft",
            "is_current": False,
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["code"] == "API-2026"


@pytest.mark.django_db
def test_teacher_cannot_manage_catalogs():
    user = make_user("docente-catalogos@example.edu", "API-002", "Docente")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/academic/periods/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_career_coordinator_reads_only_assigned_careers():
    coordinator = make_user(
        "coord-catalogos@example.edu",
        "API-003",
        "Coordinador de carrera",
    )
    assigned = make_career(code="COORD", coordinator_user=coordinator)
    make_career(code="OTHER")
    client = APIClient()
    client.force_authenticate(coordinator)

    response = client.get("/api/academic/careers/")

    assert response.status_code == 200
    assert [career["code"] for career in response.data] == [assigned.code]


@pytest.mark.django_db
def test_career_coordinator_cannot_create_catalogs():
    coordinator = make_user(
        "coord-create-catalogos@example.edu",
        "API-004",
        "Coordinador de carrera",
    )
    client = APIClient()
    client.force_authenticate(coordinator)

    response = client.post(
        "/api/academic/modalities/",
        {"code": "VIR", "name": "Virtual"},
        format="json",
    )

    assert response.status_code == 403
