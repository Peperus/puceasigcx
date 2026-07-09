from datetime import date

from apps.academic_catalogs.models import (
    AcademicDomain,
    AcademicLevel,
    AcademicPeriod,
    Career,
    CurriculumSubject,
    FacultyOrUnit,
    GradingSystem,
    Modality,
    PeriodStatus,
    StudyPlan,
    Subject,
)


def make_period(code="2026-1", is_current=False, status=PeriodStatus.DRAFT):
    return AcademicPeriod.objects.create(
        name=f"Periodo {code}",
        code=code,
        start_date=date(2026, 1, 1),
        end_date=date(2026, 6, 30),
        enrollment_start_date=date(2026, 1, 1),
        enrollment_end_date=date(2026, 1, 31),
        status=status,
        is_current=is_current,
    )


def make_modality(code="PRES"):
    return Modality.objects.create(code=code, name=f"Modalidad {code}")


def make_domain(code="DOM"):
    return AcademicDomain.objects.create(code=code, name=f"Dominio {code}")


def make_unit(code="UNIT"):
    return FacultyOrUnit.objects.create(code=code, name=f"Unidad {code}")


def make_career(code="CAR", coordinator_user=None):
    return Career.objects.create(
        code=code,
        name=f"Carrera {code}",
        faculty=make_unit(f"UNIT-{code}"),
        modality=make_modality(f"MOD-{code}"),
        domain=make_domain(f"DOM-{code}"),
        coordinator_user=coordinator_user,
    )


def make_plan(career=None, code="PLAN"):
    if career is None:
        career = make_career()
    return StudyPlan.objects.create(
        career=career,
        code=code,
        name=f"Plan {code}",
        version="2026",
        effective_from=date(2026, 1, 1),
        is_current=True,
    )


def make_level(study_plan=None, number=1):
    if study_plan is None:
        study_plan = make_plan()
    return AcademicLevel.objects.create(
        study_plan=study_plan,
        number=number,
        name=f"Nivel {number}",
        order=number,
    )


def make_grading_system(code="S1"):
    return GradingSystem.objects.create(code=code, name=f"Sistema {code}")


def make_subject(career=None, code="SUBJ-1"):
    if career is None:
        career = make_career()
    return Subject.objects.create(
        career=career,
        code=code,
        name=f"Asignatura {code}",
        total_hours=96,
        contact_hours=48,
        autonomous_hours=32,
        practical_hours=16,
        default_grading_system=make_grading_system(f"GS-{code}"),
    )


def make_curriculum_subject(study_plan=None, level=None, subject=None, order=1):
    if study_plan is None:
        study_plan = make_plan()
    if level is None:
        level = make_level(study_plan)
    if subject is None:
        subject = make_subject(study_plan.career)
    return CurriculumSubject.objects.create(
        study_plan=study_plan,
        level=level,
        subject=subject,
        order=order,
    )
