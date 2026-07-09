import pytest
from django.core.exceptions import ValidationError

from apps.audit.models import AuditLog
from apps.enrollment.models import Homologation, HomologationStatus
from apps.enrollment.services import save_homologation
from apps.enrollment.tests.factories import make_offer
from apps.people.tests.factories import make_student, make_user


@pytest.mark.django_db
def test_secretary_can_register_basic_homologation_structure():
    user = make_user("secretaria-homologacion@example.edu", "USR-S4T5", "Secretaria")
    offer = make_offer("S4T5")
    subject = offer.career.subjects.create(
        code="SUB-S4T5",
        name="Asignatura homologable",
        total_hours=96,
        contact_hours=48,
        autonomous_hours=32,
        practical_hours=16,
    )
    student = make_student(career=offer.career, student_code="EST-S4T5")

    homologation = save_homologation(
        Homologation(
            student=student,
            subject=subject,
            period=offer.period,
            resolution_reference="RES-SINT-001",
            status=HomologationStatus.REGISTERED,
        ),
        user=user,
    )

    assert homologation.registered_by == user
    assert AuditLog.objects.filter(action="homologation_registered").exists()


@pytest.mark.django_db
def test_homologation_does_not_duplicate_student_subject_period():
    offer = make_offer("S4T5DUP")
    subject = offer.career.subjects.create(
        code="SUB-S4T5DUP",
        name="Asignatura homologable",
        total_hours=96,
        contact_hours=48,
        autonomous_hours=32,
        practical_hours=16,
    )
    student = make_student(career=offer.career, student_code="EST-S4T5DUP")
    Homologation.objects.create(
        student=student,
        subject=subject,
        period=offer.period,
        resolution_reference="RES-SINT-001",
    )

    with pytest.raises(ValidationError):
        Homologation.objects.create(
            student=student,
            subject=subject,
            period=offer.period,
            resolution_reference="RES-SINT-002",
        )


@pytest.mark.django_db
def test_homologation_requires_subject_from_student_career():
    offer = make_offer("S4T5CAREER")
    other_offer = make_offer("S4T5OTHER")
    subject = other_offer.career.subjects.create(
        code="SUB-S4T5OTHER",
        name="Asignatura otra carrera",
        total_hours=96,
        contact_hours=48,
        autonomous_hours=32,
        practical_hours=16,
    )
    student = make_student(career=offer.career, student_code="EST-S4T5CAREER")

    with pytest.raises(ValidationError):
        Homologation.objects.create(
            student=student,
            subject=subject,
            period=offer.period,
            resolution_reference="RES-SINT-003",
        )
