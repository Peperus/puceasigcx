import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIClient

from apps.audit.models import AuditLog


@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        email="estudiante@example.edu",
        password="Old-pass-demo-123",
        names="Estudiante",
        last_names="Sintetico",
        identification="ID-RESET-001",
    )


@pytest.mark.django_db
def test_password_reset_request_sends_email_without_revealing_existence(user):
    client = APIClient()

    existing_response = client.post(
        reverse("password-reset"),
        {"email": user.email},
        format="json",
    )
    missing_response = client.post(
        reverse("password-reset"),
        {"email": "noexiste@example.edu"},
        format="json",
    )

    assert existing_response.status_code == 200
    assert missing_response.status_code == 200
    assert existing_response.json() == missing_response.json()
    assert len(mail.outbox) == 1
    assert "Token:" in mail.outbox[0].body


@pytest.mark.django_db
def test_password_reset_confirm_changes_password_with_valid_token(user):
    uid = urlsafe_base64_encode(str(user.pk).encode())
    token = default_token_generator.make_token(user)

    response = APIClient().post(
        reverse("password-reset-confirm"),
        {
            "uid": uid,
            "token": token,
            "new_password": "New-pass-demo-123",
        },
        format="json",
    )

    user.refresh_from_db()
    assert response.status_code == 200
    assert user.check_password("New-pass-demo-123")
    assert AuditLog.objects.filter(
        action="password_changed",
        module="authentication",
        object_id=str(user.pk),
    ).exists()


@pytest.mark.django_db
def test_password_reset_confirm_rejects_invalid_token(user):
    uid = urlsafe_base64_encode(str(user.pk).encode())

    response = APIClient().post(
        reverse("password-reset-confirm"),
        {
            "uid": uid,
            "token": "invalid-token",
            "new_password": "New-pass-demo-123",
        },
        format="json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
@override_settings(PASSWORD_RESET_TIMEOUT=-1)
def test_password_reset_confirm_rejects_expired_token(user):
    uid = urlsafe_base64_encode(str(user.pk).encode())
    token = default_token_generator.make_token(user)

    response = APIClient().post(
        reverse("password-reset-confirm"),
        {
            "uid": uid,
            "token": token,
            "new_password": "New-pass-demo-123",
        },
        format="json",
    )

    assert response.status_code == 400
