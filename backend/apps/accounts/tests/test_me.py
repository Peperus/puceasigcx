import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def user():
    user = get_user_model().objects.create_user(
        email="coordinador@example.edu",
        password="Str0ng-pass-demo",
        names="Coordinador",
        last_names="Sintetico",
        identification="ID-ME-001",
        phone="0990000000",
    )
    user.groups.add(Group.objects.create(name="Coordinador de carrera"))
    return user


@pytest.mark.django_db
def test_authenticated_user_can_get_current_profile(user):
    client = APIClient()
    client.force_authenticate(user)

    response = client.get(reverse("me"))

    assert response.status_code == 200
    assert response.json()["email"] == user.email
    assert response.json()["roles"] == ["career_coordinator"]


@pytest.mark.django_db
def test_anonymous_user_cannot_get_current_profile():
    response = APIClient().get(reverse("me"))

    assert response.status_code == 401


@pytest.mark.django_db
def test_user_can_patch_only_editable_profile_fields(user):
    client = APIClient()
    client.force_authenticate(user)

    response = client.patch(
        reverse("me"),
        {
            "names": "Nombre Editado",
            "phone": "0991111111",
            "email": "otro@example.edu",
            "roles": ["administrator"],
        },
        format="json",
    )

    user.refresh_from_db()
    payload = response.json()

    assert response.status_code == 200
    assert payload["names"] == "Nombre Editado"
    assert payload["phone"] == "0991111111"
    assert user.email == "coordinador@example.edu"
    assert payload["roles"] == ["career_coordinator"]
