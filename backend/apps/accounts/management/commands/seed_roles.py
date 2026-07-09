from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from apps.accounts.roles import (
    ROLE_ADMINISTRATOR,
    ROLE_CAREER_COORDINATOR,
    ROLE_DEFINITIONS,
    ROLE_SECRETARY,
)

PERMISSIONS_BY_ROLE = {
    ROLE_ADMINISTRATOR: {
        "accounts.add_user",
        "accounts.change_user",
        "accounts.delete_user",
        "accounts.view_user",
        "accounts.add_userprofile",
        "accounts.change_userprofile",
        "accounts.delete_userprofile",
        "accounts.view_userprofile",
        "audit.view_auditlog",
    },
    ROLE_SECRETARY: {
        "accounts.add_user",
        "accounts.change_user",
        "accounts.view_user",
        "accounts.change_userprofile",
        "accounts.view_userprofile",
        "audit.view_auditlog",
    },
    ROLE_CAREER_COORDINATOR: {
        "accounts.view_user",
        "accounts.view_userprofile",
        "audit.view_auditlog",
    },
}


class Command(BaseCommand):
    help = "Crea roles institucionales PUCEASIG de forma idempotente."

    def handle(self, *args, **options):
        created_count = 0

        for role in ROLE_DEFINITIONS:
            group, created = Group.objects.get_or_create(name=role.name)
            created_count += int(created)

            permission_labels = PERMISSIONS_BY_ROLE.get(role.code, set())
            permissions = self._get_permissions(permission_labels)
            group.permissions.add(*permissions)

        self.stdout.write(
            self.style.SUCCESS(
                f"Roles sincronizados: {len(ROLE_DEFINITIONS)} "
                f"({created_count} nuevos)."
            )
        )

    def _get_permissions(self, permission_labels):
        permissions = []
        for label in permission_labels:
            app_label, codename = label.split(".", maxsplit=1)
            try:
                permissions.append(
                    Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename,
                    )
                )
            except Permission.DoesNotExist:
                self.stderr.write(self.style.WARNING(f"Permiso no encontrado: {label}"))
        return permissions
