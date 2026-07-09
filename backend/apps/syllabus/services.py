"""Transactional services for syllabus domain."""

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.accounts.roles import (
    ROLE_ACADEMIC_DIRECTOR,
    ROLE_ADMINISTRATOR,
    ROLE_CAREER_COORDINATOR,
    ROLE_SECRETARY,
    ROLE_TEACHER,
    user_has_role,
)
from apps.audit.services import log_event
from apps.enrollment.models import TeachingAssignment

from .models import (
    AchievementLevelCode,
    LearningOutcomeType,
    Syllabus,
    SyllabusLearningOutcome,
    SyllabusStatus,
)

REQUIRED_OUTCOMES_BY_TYPE = 3
REQUIRED_ACHIEVEMENT_LEVELS = {choice.value for choice in AchievementLevelCode}


def model_validation_error_to_serializer_error(exc):
    if hasattr(exc, "message_dict"):
        return exc.message_dict
    if hasattr(exc, "messages"):
        return {"non_field_errors": exc.messages}
    return {"non_field_errors": [str(exc)]}


def user_is_assigned_teacher(user, syllabus):
    if not getattr(user, "is_authenticated", False):
        return False
    return TeachingAssignment.objects.filter(
        course_section=syllabus.course_section,
        teacher__person__user=user,
    ).exists()


def user_can_edit_syllabus(user, syllabus):
    if user_has_role(user, ROLE_ADMINISTRATOR):
        return syllabus.is_editable
    return (
        syllabus.is_editable
        and user_has_role(user, ROLE_TEACHER)
        and user_is_assigned_teacher(user, syllabus)
    )


def user_can_approve_syllabus(user, syllabus):
    if user_has_role(user, ROLE_ADMINISTRATOR, ROLE_SECRETARY, ROLE_ACADEMIC_DIRECTOR):
        return True
    if user_has_role(user, ROLE_CAREER_COORDINATOR):
        return syllabus.course_section.offer.career.coordinator_user_id == user.id
    return False


def user_can_upload_signed_syllabus(user, syllabus):
    return user_can_approve_syllabus(user, syllabus) or user_is_assigned_teacher(
        user, syllabus
    )


def _snapshot(syllabus):
    return {
        "id": syllabus.pk,
        "course_section_id": syllabus.course_section_id,
        "status": syllabus.status,
        "version": syllabus.version,
        "lead_teacher_id": syllabus.lead_teacher_id,
        "co_teacher_id": syllabus.co_teacher_id,
    }


def _log_syllabus_event(
    *,
    syllabus,
    action,
    user=None,
    request=None,
    previous_data=None,
    reason="",
):
    return log_event(
        action=action,
        module="syllabus",
        user=user,
        model_name=Syllabus.__name__,
        object_id=syllabus.pk,
        previous_data=previous_data or {},
        new_data=_snapshot(syllabus),
        reason=reason,
        request=request,
    )


@transaction.atomic
def save_syllabus(syllabus, *, user=None, request=None):
    created = syllabus.pk is None
    previous = {}
    if created and user is not None:
        syllabus.created_by = user
    elif syllabus.pk:
        previous = _snapshot(Syllabus.objects.get(pk=syllabus.pk))

    syllabus.full_clean()
    syllabus.save()
    _log_syllabus_event(
        syllabus=syllabus,
        action="syllabus_created" if created else "syllabus_updated",
        user=user,
        request=request,
        previous_data=previous,
    )
    return syllabus


def validate_learning_outcomes_ready(syllabus):
    errors = {}
    for outcome_type in LearningOutcomeType:
        count = syllabus.syllabuslearningoutcomes.filter(
            outcome_type=outcome_type.value
        ).count()
        if count < REQUIRED_OUTCOMES_BY_TYPE:
            errors[outcome_type.value] = (
                f"Registre al menos {REQUIRED_OUTCOMES_BY_TYPE} resultados "
                f"de aprendizaje de {outcome_type.label.lower()}."
            )
    if errors:
        raise ValidationError(errors)


def validate_rubrics_ready(syllabus):
    validate_learning_outcomes_ready(syllabus)
    errors = {}
    subject_outcomes = syllabus.syllabuslearningoutcomes.filter(
        outcome_type=LearningOutcomeType.SUBJECT
    ).prefetch_related("criteria__achievement_levels")
    for outcome in subject_outcomes:
        criteria = list(outcome.criteria.all())
        if not criteria:
            errors[f"outcome_{outcome.pk}"] = (
                f"El RA de asignatura {outcome.order} no tiene criterios."
            )
            continue
        total_weight = sum((criterion.weight for criterion in criteria), Decimal("0"))
        if total_weight != Decimal("100.00"):
            errors[f"outcome_{outcome.pk}_weight"] = (
                f"Los criterios del RA {outcome.order} deben sumar 100."
            )
        for criterion in criteria:
            levels = {level.level for level in criterion.achievement_levels.all()}
            if levels != REQUIRED_ACHIEVEMENT_LEVELS:
                errors[f"criterion_{criterion.pk}_levels"] = (
                    "Cada criterio debe tener niveles A, B, C y D."
                )
    if errors:
        raise ValidationError(errors)


def validate_syllabus_complete(syllabus):
    errors = {}
    if not syllabus.subject_description.strip():
        errors["subject_description"] = (
            "La descripcion de la asignatura es obligatoria."
        )
    if not syllabus.methodology.strip():
        errors["methodology"] = "La metodologia es obligatoria."
    if not syllabus.syllabuscompetencys.exists():
        errors["competencies"] = "Registre al menos una competencia."
    if not syllabus.syllabusbibliographys.exists():
        errors["bibliography"] = "Registre bibliografia minima."
    if not syllabus.syllabusweeklyplans.exists():
        errors["weekly_plan"] = "Registre planificacion semanal minima."
    try:
        validate_rubrics_ready(syllabus)
    except ValidationError as exc:
        if hasattr(exc, "message_dict"):
            errors.update(exc.message_dict)
        else:
            errors["rubrics"] = exc.messages
    if errors:
        raise ValidationError(errors)


@transaction.atomic
def finalize_syllabus(syllabus, *, user=None, request=None):
    if syllabus.status not in {SyllabusStatus.DRAFT, SyllabusStatus.OBSERVED}:
        raise ValidationError(
            {"status": "Solo se puede finalizar un silabo en borrador u observado."}
        )
    validate_syllabus_complete(syllabus)
    previous = _snapshot(syllabus)
    syllabus.status = SyllabusStatus.FINALIZED
    syllabus.finalized_at = timezone.now()
    syllabus.save()
    _log_syllabus_event(
        syllabus=syllabus,
        action="syllabus_finalized",
        user=user,
        request=request,
        previous_data=previous,
    )
    return syllabus


@transaction.atomic
def submit_syllabus(syllabus, *, user=None, request=None):
    if syllabus.status not in {SyllabusStatus.FINALIZED, SyllabusStatus.OBSERVED}:
        raise ValidationError(
            {"status": "Solo se puede enviar un silabo finalizado u observado."}
        )
    validate_syllabus_complete(syllabus)
    previous = _snapshot(syllabus)
    syllabus.status = SyllabusStatus.IN_REVIEW
    syllabus.submitted_at = timezone.now()
    syllabus.save()
    _log_syllabus_event(
        syllabus=syllabus,
        action="syllabus_submitted",
        user=user,
        request=request,
        previous_data=previous,
    )
    return syllabus


@transaction.atomic
def approve_syllabus(syllabus, *, user=None, request=None):
    if syllabus.status != SyllabusStatus.IN_REVIEW:
        raise ValidationError(
            {"status": "Solo se puede aprobar un silabo en revision."}
        )
    if user_is_assigned_teacher(user, syllabus) and not user_has_role(
        user, ROLE_ADMINISTRATOR, ROLE_ACADEMIC_DIRECTOR
    ):
        raise ValidationError(
            {"user": "El docente asignado no puede aprobar su propio silabo."}
        )
    if not user_can_approve_syllabus(user, syllabus):
        raise ValidationError({"user": "No tiene permiso para aprobar este silabo."})
    previous = _snapshot(syllabus)
    syllabus.status = SyllabusStatus.APPROVED
    syllabus.approved_at = timezone.now()
    syllabus.approved_by = user
    syllabus.save()
    _log_syllabus_event(
        syllabus=syllabus,
        action="syllabus_approved",
        user=user,
        request=request,
        previous_data=previous,
    )
    return syllabus


@transaction.atomic
def observe_syllabus(syllabus, *, reason, user=None, request=None):
    if not reason.strip():
        raise ValidationError({"reason": "La observacion es obligatoria."})
    if syllabus.status != SyllabusStatus.IN_REVIEW:
        raise ValidationError(
            {"status": "Solo se puede observar un silabo en revision."}
        )
    if not user_can_approve_syllabus(user, syllabus):
        raise ValidationError({"user": "No tiene permiso para observar este silabo."})
    previous = _snapshot(syllabus)
    syllabus.status = SyllabusStatus.OBSERVED
    syllabus.save()
    _log_syllabus_event(
        syllabus=syllabus,
        action="syllabus_observed",
        user=user,
        request=request,
        previous_data=previous,
        reason=reason,
    )
    return syllabus


@transaction.atomic
def reopen_syllabus(syllabus, *, reason, user=None, request=None):
    if not reason.strip():
        raise ValidationError({"reason": "La justificacion es obligatoria."})
    if not user_can_approve_syllabus(user, syllabus):
        raise ValidationError({"user": "No tiene permiso para reabrir este silabo."})
    if syllabus.status not in {
        SyllabusStatus.APPROVED,
        SyllabusStatus.FINALIZED,
        SyllabusStatus.IN_REVIEW,
        SyllabusStatus.OBSERVED,
    }:
        raise ValidationError({"status": "Este silabo no requiere reapertura."})
    previous = _snapshot(syllabus)
    syllabus.status = SyllabusStatus.DRAFT
    syllabus.approved_at = None
    syllabus.approved_by = None
    syllabus.save()
    _log_syllabus_event(
        syllabus=syllabus,
        action="syllabus_reopened",
        user=user,
        request=request,
        previous_data=previous,
        reason=reason,
    )
    return syllabus


@transaction.atomic
def upload_signed_syllabus(syllabus, *, signed_file, user=None, request=None):
    if syllabus.status != SyllabusStatus.APPROVED:
        raise ValidationError(
            {"status": "Solo se puede cargar PDF firmado en un silabo aprobado."}
        )
    if not user_can_upload_signed_syllabus(user, syllabus):
        raise ValidationError({"user": "No tiene permiso para cargar el archivo."})
    max_size = getattr(settings, "SYLLABUS_SIGNED_FILE_MAX_BYTES", 5 * 1024 * 1024)
    if signed_file.size > max_size:
        raise ValidationError(
            {
                "signed_file": (
                    f"El archivo supera el maximo permitido de {max_size} bytes."
                )
            }
        )
    if not signed_file.name.lower().endswith(".pdf"):
        raise ValidationError({"signed_file": "El archivo debe ser PDF."})

    previous = _snapshot(syllabus)
    syllabus.signed_file = signed_file
    syllabus.signed_file_uploaded_by = user
    syllabus.signed_file_uploaded_at = timezone.now()
    syllabus.save()
    _log_syllabus_event(
        syllabus=syllabus,
        action="syllabus_signed_file_uploaded",
        user=user,
        request=request,
        previous_data=previous,
    )
    return syllabus


def is_syllabus_ready_for_grading(course_section):
    return Syllabus.objects.filter(
        course_section=course_section,
        status=SyllabusStatus.APPROVED,
    ).exists()


def syllabus_print_context(syllabus):
    outcomes = SyllabusLearningOutcome.objects.filter(
        syllabus=syllabus
    ).prefetch_related("criteria__achievement_levels")
    return {
        "syllabus": syllabus,
        "course": syllabus.course_section,
        "offer": syllabus.course_section.offer,
        "subject": syllabus.course_section.subject,
        "competencies": syllabus.syllabuscompetencys.all(),
        "learning_outcomes": outcomes,
        "bibliography": syllabus.syllabusbibliographys.all(),
        "weekly_plan": syllabus.syllabusweeklyplans.select_related("learning_outcome"),
    }
