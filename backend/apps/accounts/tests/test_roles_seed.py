import pytest
from django.contrib.auth.models import Group
from django.core.management import call_command

from apps.accounts.roles import ROLE_DEFINITIONS


@pytest.mark.django_db
def test_seed_roles_creates_institutional_groups_idempotently():
    call_command("seed_roles")
    call_command("seed_roles")

    expected_names = {role.name for role in ROLE_DEFINITIONS}

    assert set(Group.objects.values_list("name", flat=True)) == expected_names
    assert Group.objects.count() == len(ROLE_DEFINITIONS)


@pytest.mark.django_db
def test_seed_roles_assigns_base_permissions_to_administrator():
    call_command("seed_roles")

    administrator = Group.objects.get(name="Administrador")
    permission_labels = {
        f"{permission.content_type.app_label}.{permission.codename}"
        for permission in administrator.permissions.all()
    }

    assert "accounts.add_user" in permission_labels
    assert "accounts.change_user" in permission_labels
    assert "audit.view_auditlog" in permission_labels
