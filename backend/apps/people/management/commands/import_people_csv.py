from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.people.services import import_people_csv


class Command(BaseCommand):
    help = "Importa personas, estudiantes y docentes desde un CSV sintetico."

    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("--user-email", default="")
        parser.add_argument(
            "--strict",
            action="store_true",
            help="Detiene la importacion ante el primer error de fila.",
        )
        parser.add_argument(
            "--no-update",
            action="store_true",
            help="Rechaza filas que intenten actualizar registros existentes.",
        )

    def handle(self, *args, **options):
        user = None
        if options["user_email"]:
            user = (
                get_user_model()
                .objects.filter(email__iexact=options["user_email"])
                .first()
            )
            if user is None:
                raise CommandError("No existe un usuario con ese correo.")

        result = import_people_csv(
            options["path"],
            user=user,
            update_existing=not options["no_update"],
            tolerate_errors=not options["strict"],
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Importacion completada: "
                f"{result.created} creados, "
                f"{result.updated} actualizados, "
                f"{result.rejected} rechazados."
            )
        )
        for error in result.errors:
            self.stderr.write(f"Fila {error.row_number}: {error.message}")
