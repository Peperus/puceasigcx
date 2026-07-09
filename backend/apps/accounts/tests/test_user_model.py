import pytest
from django.contrib.auth import get_user_model

from apps.accounts.models import UserProfile


@pytest.mark.django_db
def test_user_uses_institutional_email_as_identifier():
    user = get_user_model().objects.create_user(
        email="DOCENTE.UNO@example.edu",
        password="Str0ng-pass-demo",
        names="Nombre",
        last_names="Sintetico",
        identification="ID-001",
    )

    assert user.email == "docente.uno@example.edu"
    assert user.USERNAME_FIELD == "email"
    assert user.check_password("Str0ng-pass-demo")
    assert user.full_name == "Nombre Sintetico"
    assert UserProfile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_superuser_flags_are_required():
    user = get_user_model().objects.create_superuser(
        email="admin@example.edu",
        password="Str0ng-pass-demo",
        names="Admin",
        last_names="Sintetico",
        identification="ID-ADM",
    )

    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.is_active is True


@pytest.mark.django_db
def test_user_requires_email():
    with pytest.raises(ValueError, match="correo institucional"):
        get_user_model().objects.create_user(
            email="",
            password="Str0ng-pass-demo",
            names="Sin",
            last_names="Correo",
            identification="ID-002",
        )
