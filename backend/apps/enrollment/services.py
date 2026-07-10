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


def _offer_snapshot(offer):
    return {
        "id": offer.pk,
        "period_id": offer.period_id,
        "career_id": offer.career_id,
        "study_plan_id": offer.study_plan_id,
        "level_id": offer.level_id,
        "status": offer.status,
    }


def _course_section_snapshot(course_section):
    return {
        "id": course_section.pk,
        "offer_id": course_section.offer_id,
        "subject_id": course_section.subject_id,
        "parallel": course_section.parallel,
        "capacity": course_section.capacity,
        "status": course_section.status,
        "grading_system_id": course_section.grading_system_id,
    }


def _teaching_assignment_snapshot(assignment):
    return {
        "id": assignment.pk,
        "course_section_id": assignment.course_section_id,
        "teacher_id": assignment.teacher_id,
        "role": assignment.role,
        "status": assignment.status,
        "weekly_hours": (
            str(assignment.weekly_hours)
            if assignment.weekly_hours is not None
            else None
        ),
    }


@transaction.atomic
def save_academic_offer(instance, *, user=None, request=None):
    created = instance.pk is None
    previous = (
        {}
        if created
        else _offer_snapshot(
            AcademicOffer.objects.select_for_update().get(pk=instance.pk)
        )
    )
    offer = _save_instance(instance)
    log_event(
        action="academic_offer_created" if created else "academic_offer_updated",
        module="enrollment",
        user=user,
        model_name=AcademicOffer.__name__,
        object_id=offer.pk,
        previous_data=previous,
        new_data=_offer_snapshot(offer),
        request=request,
    )
    return offer


@transaction.atomic
def save_course_section(instance, *, user=None, request=None):
    created = instance.pk is None
    previous = (
        {}
        if created
        else _course_section_snapshot(
            CourseSection.objects.select_for_update().get(pk=instance.pk)
        )
    )
    course_section = _save_instance(instance)
    log_event(
        action="course_section_created" if created else "course_section_updated",
        module="enrollment",
        user=user,
        model_name=CourseSection.__name__,
        object_id=course_section.pk,
        previous_data=previous,
        new_data=_course_section_snapshot(course_section),
        request=request,
    )
    return course_section


@transaction.atomic
def save_teaching_assignment(instance, *, user=None, request=None):
    created = instance.pk is None
    previous = (
        {}
        if created
        else _teaching_assignment_snapshot(
            TeachingAssignment.objects.select_for_update().get(pk=instance.pk)
        )
    )
    assignment = _save_instance(instance)
    log_event(
        action=(
            "teaching_assignment_created" if created else "teaching_assignment_updated"
        ),
        module="enrollment",
        user=user,
        model_name=TeachingAssignment.__name__,
        object_id=assignment.pk,
        previous_data=previous,
        new_data=_teaching_assignment_snapshot(assignment),
        request=request,
    )
    return assignment


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
