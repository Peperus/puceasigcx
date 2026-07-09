import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APIClient

from apps.audit.models import AuditLog


@pytest.mark.django_db
def test_user_creation_is_audited():
    user = get_user_model().objects.create_user(
        email="audit-user@example.edu",
        password="Str0ng-pass-demo",
        names="Auditado",
        last_names="Sintetico",
        identification="ID-AUDIT-001",
    )

    assert AuditLog.objects.filter(
        action="user_created",
        module="accounts",
        model_name="User",
        object_id=str(user.pk),
    ).exists()


@pytest.mark.django_db
def test_role_change_is_audited():
    user = get_user_model().objects.create_user(
        email="audit-role@example.edu",
        password="Str0ng-pass-demo",
        names="Rol",
        last_names="Sintetico",
        identification="ID-AUDIT-002",
    )
    group = Group.objects.create(name="Docente")

    user.groups.add(group)

    assert AuditLog.objects.filter(
        action="role_changed",
        module="accounts",
        object_id=str(user.pk),
    ).exists()
    user.profile.refresh_from_db()
    assert user.profile.primary_role == "Docente"


@pytest.mark.django_db
def test_failed_login_is_audited():
    user = get_user_model().objects.create_user(
        email="audit-login@example.edu",
        password="Str0ng-pass-demo",
        names="Login",
        last_names="Sintetico",
        identification="ID-AUDIT-003",
    )

    response = APIClient().post(
        reverse("auth-login"),
        {"email": user.email, "password": "incorrecta"},
        format="json",
    )

    assert response.status_code == 401
    assert AuditLog.objects.filter(
        action="login_failed",
        module="authentication",
        object_id=str(user.pk),
    ).exists()
