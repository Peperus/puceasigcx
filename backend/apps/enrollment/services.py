"""Transactional services for enrollment domain."""

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.audit.services import log_event

from .models import (
    AcademicOffer,
    CourseEnrollment,
    CourseSection,
    Enrollment,
    Homologation,
    TeachingAssignment,
)


def _save_instance(instance):
    instance.full_clean()
    instance.save()
    return instance


@transaction.atomic
def save_academic_offer(instance):
    return _save_instance(instance)


@transaction.atomic
def save_course_section(instance):
    return _save_instance(instance)


@transaction.atomic
def save_teaching_assignment(instance):
    return _save_instance(instance)


@transaction.atomic
def save_enrollment(instance, *, user=None, request=None):
    created = instance.pk is None
    if created and user is not None:
        instance.created_by = user
    enrollment = _save_instance(instance)
    log_event(
        action="enrollment_created" if created else "enrollment_updated",
        module="enrollment",
        user=user,
        model_name=Enrollment.__name__,
        object_id=enrollment.pk,
        new_data={
            "student_id": enrollment.student_id,
            "period_id": enrollment.period_id,
            "career_id": enrollment.career_id,
            "status": enrollment.status,
        },
        request=request,
    )
    return enrollment


@transaction.atomic
def save_course_enrollment(instance, *, user=None, request=None):
    created = instance.pk is None
    course_enrollment = _save_instance(instance)
    log_event(
        action="course_enrollment_created" if created else "course_enrollment_updated",
        module="enrollment",
        user=user,
        model_name=CourseEnrollment.__name__,
        object_id=course_enrollment.pk,
        new_data={
            "enrollment_id": course_enrollment.enrollment_id,
            "course_section_id": course_enrollment.course_section_id,
            "status": course_enrollment.status,
        },
        request=request,
    )
    return course_enrollment


@transaction.atomic
def save_homologation(instance, *, user=None, request=None):
    created = instance.pk is None
    if created and user is not None:
        instance.registered_by = user
    homologation = _save_instance(instance)
    log_event(
        action="homologation_registered" if created else "homologation_updated",
        module="enrollment",
        user=user,
        model_name=Homologation.__name__,
        object_id=homologation.pk,
        new_data={
            "student_id": homologation.student_id,
            "subject_id": homologation.subject_id,
            "period_id": homologation.period_id,
            "status": homologation.status,
        },
        request=request,
    )
    return homologation


def model_validation_error_to_serializer_error(exc):
    if hasattr(exc, "message_dict"):
        return exc.message_dict
    if hasattr(exc, "messages"):
        return {"non_field_errors": exc.messages}
    return {"non_field_errors": [str(exc)]}


MODEL_SERVICE_BY_CLASS = {
    AcademicOffer: save_academic_offer,
    CourseSection: save_course_section,
    TeachingAssignment: save_teaching_assignment,
}


def save_non_audited_instance(instance):
    try:
        service = MODEL_SERVICE_BY_CLASS[type(instance)]
    except KeyError as exc:
        raise ValidationError("Modelo no soportado por el servicio.") from exc
    return service(instance)
