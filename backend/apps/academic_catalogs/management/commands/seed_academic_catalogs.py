from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.academic_catalogs.models import (
    AcademicDomain,
    AcademicLevel,
    AcademicPeriod,
    Career,
    CurriculumPrerequisite,
    CurriculumSubject,
    FacultyOrUnit,
    Modality,
    PeriodStatus,
    StudyPlan,
    Subject,
)
from apps.academic_catalogs.services import ensure_default_academic_setting


class Command(BaseCommand):
    help = "Crea catalogos academicos sinteticos para desarrollo y pruebas."

    @transaction.atomic
    def handle(self, *args, **options):
        setting = ensure_default_academic_setting()

        unit, _ = FacultyOrUnit.objects.update_or_create(
            code="UAC-DEMO",
            defaults={
                "name": "Unidad Academica Demo",
                "description": "Unidad sintetica para pruebas del MVP.",
            },
        )
        modality, _ = Modality.objects.update_or_create(
            code="PRES",
            defaults={"name": "Presencial", "description": "Modalidad presencial."},
        )
        domain, _ = AcademicDomain.objects.update_or_create(
            code="DOM-GEN",
            defaults={
                "name": "Dominio Academico General",
                "description": "Dominio sintetico para catalogos base.",
            },
        )
        period, _ = AcademicPeriod.objects.update_or_create(
            code="2026-1",
            defaults={
                "name": "Periodo Academico Demo 2026-1",
                "start_date": date(2026, 1, 1),
                "end_date": date(2026, 6, 30),
                "enrollment_start_date": date(2026, 1, 5),
                "enrollment_end_date": date(2026, 1, 20),
                "status": PeriodStatus.ACTIVE,
                "is_current": True,
            },
        )
        career, _ = Career.objects.update_or_create(
            code="CAR-DEMO",
            defaults={
                "name": "Carrera Demo de Gestion Academica",
                "faculty": unit,
                "modality": modality,
                "domain": domain,
                "description": "Carrera sintetica sin datos personales.",
            },
        )
        plan, _ = StudyPlan.objects.update_or_create(
            career=career,
            code="PLAN-2026",
            defaults={
                "name": "Plan de Estudios Demo 2026",
                "version": "2026",
                "effective_from": date(2026, 1, 1),
                "is_current": True,
            },
        )
        level_1, _ = AcademicLevel.objects.update_or_create(
            study_plan=plan,
            number=1,
            defaults={"name": "Primer nivel", "order": 1},
        )
        level_2, _ = AcademicLevel.objects.update_or_create(
            study_plan=plan,
            number=2,
            defaults={"name": "Segundo nivel", "order": 2},
        )

        subject_intro, _ = Subject.objects.update_or_create(
            career=career,
            code="DEMO-101",
            defaults={
                "name": "Introduccion a Procesos Academicos",
                "total_hours": 96,
                "contact_hours": 48,
                "autonomous_hours": 32,
                "practical_hours": 16,
                "default_grading_system": setting.default_grading_system,
            },
        )
        subject_methods, _ = Subject.objects.update_or_create(
            career=career,
            code="DEMO-201",
            defaults={
                "name": "Metodos de Gestion Academica",
                "total_hours": 96,
                "contact_hours": 48,
                "autonomous_hours": 32,
                "practical_hours": 16,
                "default_grading_system": setting.default_grading_system,
            },
        )
        curriculum_intro, _ = CurriculumSubject.objects.update_or_create(
            study_plan=plan,
            subject=subject_intro,
            defaults={"level": level_1, "domain": domain, "order": 1, "credits": 3},
        )
        curriculum_methods, _ = CurriculumSubject.objects.update_or_create(
            study_plan=plan,
            subject=subject_methods,
            defaults={"level": level_2, "domain": domain, "order": 1, "credits": 3},
        )
        CurriculumPrerequisite.objects.get_or_create(
            curriculum_subject=curriculum_methods,
            prerequisite=curriculum_intro,
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Catalogos academicos sincronizados: "
                f"{period.code}, {career.code}, {plan.code}."
            )
        )
