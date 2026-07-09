import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def active_user():
    user = get_user_model().objects.create_user(
        email="docente@example.edu",
        password="Str0ng-pass-demo",
        names="Docente",
        last_names="Sintetico",
        identification="ID-JWT-001",
    )
    group = Group.objects.create(name="Docente")
    user.groups.add(group)
    return user


@pytest.mark.django_db
def test_login_returns_access_refresh_and_user_roles(active_user):
    response = APIClient().post(
        reverse("auth-login"),
        {"email": active_user.email, "password": "Str0ng-pass-demo"},
        format="json",
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["access"]
    assert payload["refresh"]
    assert payload["user"]["email"] == active_user.email
    assert payload["user"]["roles"] == ["teacher"]


@pytest.mark.django_db
def test_login_rejects_wrong_password(active_user):
    response = APIClient().post(
        reverse("auth-login"),
        {"email": active_user.email, "password": "wrong-password"},
        format="json",
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_login_rejects_inactive_user():
    user = get_user_model().objects.create_user(
        email="inactivo@example.edu",
        password="Str0ng-pass-demo",
        names="Usuario",
        last_names="Inactivo",
        identification="ID-JWT-002",
        is_active=False,
    )

    response = APIClient().post(
        reverse("auth-login"),
        {"email": user.email, "password": "Str0ng-pass-demo"},
        format="json",
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_refresh_returns_new_access_token(active_user):
    client = APIClient()
    login_response = client.post(
        reverse("auth-login"),
        {"email": active_user.email, "password": "Str0ng-pass-demo"},
        format="json",
    )

    response = client.post(
        reverse("auth-refresh"),
        {"refresh": login_response.json()["refresh"]},
        format="json",
    )

    assert response.status_code == 200
    assert response.json()["access"]


@pytest.mark.django_db
def test_logout_blacklists_refresh_token(active_user):
    client = APIClient()
    login_response = client.post(
        reverse("auth-login"),
        {"email": active_user.email, "password": "Str0ng-pass-demo"},
        format="json",
    )
    client.force_authenticate(active_user)

    response = client.post(
        reverse("auth-logout"),
        {"refresh": login_response.json()["refresh"]},
        format="json",
    )

    assert response.status_code == 204
