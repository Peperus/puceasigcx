"""Transactional services and calculation engines for grading domain."""

from decimal import ROUND_HALF_UP, Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.academic_catalogs.models import AcademicSetting, AchievementLevel
from apps.audit.services import log_event

from .models import (
    Gradebook,
    GradebookStatus,
    GradeCalculationSnapshot,
    GradeFinalStatus,
    GradeItem,
    GradeItemType,
    GradeRecordStatus,
    GradingModel,
    StudentGradeRecord,
)

SCALE_MIN = Decimal("0.00")
SCALE_MAX = Decimal("50.00")
PASSING_SCORE = Decimal("30.00")
RULE_VERSION = "S6.1"


def to_decimal(value):
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def validate_score(score, *, minimum=SCALE_MIN, maximum=SCALE_MAX):
    score = to_decimal(score)
    if score < minimum or score > maximum:
        raise ValidationError(
            {"score": f"La nota debe estar entre {minimum} y {maximum}."}
        )
    return score


def _default_setting():
    try:
        return AcademicSetting.objects.filter(is_default=True).first()
    except RuntimeError:
        return None


def letter_from_score(score, *, setting=None):
    score = validate_score(score)
    setting = setting or _default_setting()
    if setting is not None:
        minimum = to_decimal(setting.score_min)
        maximum = to_decimal(setting.score_max)
        validate_score(score, minimum=minimum, maximum=maximum)
        level = (
            AchievementLevel.objects.filter(
                setting=setting,
                min_score__lte=score,
                max_score__gte=score,
            )
            .order_by("-min_score")
            .first()
        )
        if level is not None:
            return level.letter

    if score >= Decimal("45.00"):
        return "A"
    if score >= Decimal("40.00"):
        return "B"
    if score >= Decimal("30.00"):
        return "C"
    return "D"


def _average(scores):
    values = [validate_score(score) for score in scores]
    if not values:
        raise ValidationError({"scores": "Se requiere al menos una nota."})
    return (sum(values, Decimal("0.00")) / Decimal(len(values))).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def _weight_as_fraction(weight):
    weight = to_decimal(weight)
    if weight < 0:
        raise ValidationError({"weight": "La ponderacion no puede ser negativa."})
    return weight / Decimal("100.00") if weight > 1 else weight


def _validate_weights(items, *, label):
    total = sum(
        (_weight_as_fraction(item.get("weight", 0)) for item in items), Decimal("0")
    )
    if total != Decimal("1.00"):
        raise ValidationError({label: "Las ponderaciones deben sumar 100%."})


def _criterion_score(criterion):
    if "score" in criterion and criterion["score"] is not None:
        return validate_score(criterion["score"])
    activities = criterion.get("activities") or []
    if not activities:
        raise ValidationError({"criterion": "El criterio no tiene notas registradas."})
    return _average([activity["score"] for activity in activities])


def _learning_outcome_score(outcome):
    criteria = outcome.get("criteria") or []
    if not criteria:
        raise ValidationError({"learning_outcome": "El RA no tiene criterios."})
    _validate_weights(criteria, label="criteria")
    total = Decimal("0.00")
    for criterion in criteria:
        total += _criterion_score(criterion) * _weight_as_fraction(
            criterion.get("weight", 0)
        )
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_s1_grade(learning_outcomes, *, config=None):
    config = config or {}
    passing_score = to_decimal(config.get("passing_score", PASSING_SCORE))
    recovery_contribution = _weight_as_fraction(
        config.get("s1_recovery_contribution", Decimal("15.00"))
    )
    recovery_cap = to_decimal(config.get("recovery_cap", passing_score))

    results = []
    for order, outcome in enumerate(learning_outcomes, start=1):
        original_score = _learning_outcome_score(outcome)
        recovery_score = outcome.get("recovery_score")
        final_score = original_score
        status = "achieved" if original_score >= passing_score else "not_achieved"

        if original_score < passing_score and recovery_score is not None:
            recovery_score = validate_score(recovery_score)
            final_score = min(
                original_score + (recovery_score * recovery_contribution),
                recovery_cap,
            ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            status = "recovered" if final_score >= passing_score else "not_recovered"

        results.append(
            {
                "order": outcome.get("order", order),
                "original_score": original_score,
                "recovery_score": recovery_score,
                "final_score": final_score,
                "letter": letter_from_score(final_score),
                "status": status,
            }
        )

    failed_count = sum(1 for result in results if result["final_score"] < passing_score)
    final_score = _average([result["final_score"] for result in results])
    final_status = (
        GradeFinalStatus.APPROVED
        if failed_count == 0
        else GradeFinalStatus.INTERSEMESTRAL
    )
    return {
        "grading_model": GradingModel.S1,
        "learning_outcomes": results,
        "final_score": final_score,
        "final_letter": letter_from_score(final_score),
        "final_status": final_status,
        "failed_learning_outcomes_count": failed_count,
        "recovery_required": failed_count > 0,
    }


def calculate_s2_grade(learning_outcomes, *, config=None):
    config = config or {}
    passing_score = to_decimal(config.get("passing_score", PASSING_SCORE))
    scored_outcomes = []
    for order, outcome in enumerate(learning_outcomes, start=1):
        original_score = _learning_outcome_score(outcome)
        scored_outcomes.append(
            {
                "input": outcome,
                "order": outcome.get("order", order),
                "original_score": original_score,
                "recovery_score": outcome.get("recovery_score"),
                "final_score": original_score,
                "status": (
                    "achieved" if original_score >= passing_score else "not_achieved"
                ),
            }
        )

    failed_original = [
        outcome
        for outcome in scored_outcomes
        if outcome["original_score"] < passing_score
    ]

    final_status = GradeFinalStatus.APPROVED
    recovery_required = False
    if len(failed_original) == 1:
        recovery_required = True
        pending = failed_original[0]
        recovery_score = pending["recovery_score"]
        final_status = GradeFinalStatus.RECOVERY_REQUIRED
        if recovery_score is not None:
            recovery_score = validate_score(recovery_score)
            pending["recovery_score"] = recovery_score
            if recovery_score >= passing_score:
                pending["final_score"] = passing_score
                pending["status"] = "recovered"
                final_status = GradeFinalStatus.APPROVED
            else:
                pending["status"] = "not_recovered"
                final_status = GradeFinalStatus.FAILED
    elif len(failed_original) >= 2:
        final_status = GradeFinalStatus.FAILED

    results = []
    for outcome in scored_outcomes:
        results.append(
            {
                "order": outcome["order"],
                "original_score": outcome["original_score"],
                "recovery_score": outcome["recovery_score"],
                "final_score": outcome["final_score"],
                "letter": letter_from_score(outcome["final_score"]),
                "status": outcome["status"],
            }
        )

    failed_count = sum(1 for result in results if result["final_score"] < passing_score)
    final_score = _average([result["final_score"] for result in results])
    return {
        "grading_model": GradingModel.S2,
        "learning_outcomes": results,
        "final_score": final_score,
        "final_letter": letter_from_score(final_score),
        "final_status": final_status,
        "failed_learning_outcomes_count": failed_count,
        "recovery_required": recovery_required
        and final_status == GradeFinalStatus.RECOVERY_REQUIRED,
    }


def _practice_score(activities):
    if not activities:
        raise ValidationError({"activities": "El parcial no tiene actividades."})
    _validate_weights(activities, label="practice_activities")
    total = Decimal("0.00")
    for activity in activities:
        total += validate_score(activity["score"]) * _weight_as_fraction(
            activity.get("weight", 0)
        )
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_s3_grade(partials, *, final_evaluation_score=None, config=None):
    config = config or {}
    passing_score = to_decimal(config.get("passing_score", PASSING_SCORE))
    practice_weight = _weight_as_fraction(config.get("practice_weight", Decimal("50")))
    evaluation_weight = _weight_as_fraction(
        config.get("evaluation_weight", Decimal("50"))
    )
    if practice_weight + evaluation_weight != Decimal("1.00"):
        raise ValidationError({"components": "Practica y evaluacion deben sumar 100%."})

    partial_results = []
    for order, partial in enumerate(partials, start=1):
        practice = _practice_score(partial.get("practice_activities") or [])
        evaluation = validate_score(partial["evaluation_score"])
        partial_score = (
            practice * practice_weight + evaluation * evaluation_weight
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        partial_results.append(
            {
                "order": partial.get("order", order),
                "practice_score": practice,
                "evaluation_score": evaluation,
                "partial_score": partial_score,
                "letter": letter_from_score(partial_score),
            }
        )

    preliminary_score = _average(
        [partial["partial_score"] for partial in partial_results]
    )
    final_score = preliminary_score
    recovery_required = preliminary_score < passing_score
    final_status = (
        GradeFinalStatus.APPROVED
        if preliminary_score >= passing_score
        else GradeFinalStatus.RECOVERY_REQUIRED
    )

    final_evaluation = None
    if recovery_required and final_evaluation_score is not None:
        final_evaluation = validate_score(final_evaluation_score)
        if final_evaluation >= passing_score:
            final_score = passing_score
            final_status = GradeFinalStatus.APPROVED
            recovery_required = False
        else:
            final_status = GradeFinalStatus.FAILED

    return {
        "grading_model": GradingModel.S3,
        "partials": partial_results,
        "preliminary_score": preliminary_score,
        "final_evaluation_score": final_evaluation,
        "final_score": final_score,
        "final_letter": letter_from_score(final_score),
        "final_status": final_status,
        "failed_learning_outcomes_count": 0,
        "recovery_required": recovery_required,
    }


def _gradebook_snapshot(gradebook):
    return {
        "id": gradebook.pk,
        "course_section_id": gradebook.course_section_id,
        "syllabus_id": gradebook.syllabus_id,
        "grading_model": gradebook.grading_model,
        "status": gradebook.status,
    }


@transaction.atomic
def create_gradebook(*, course_section, syllabus, user=None, request=None):
    gradebook = Gradebook(course_section=course_section, syllabus=syllabus)
    gradebook.save()
    log_event(
        action="gradebook_created",
        module="grading",
        user=user,
        model_name=Gradebook.__name__,
        object_id=gradebook.pk,
        new_data=_gradebook_snapshot(gradebook),
        request=request,
    )
    return gradebook


@transaction.atomic
def open_gradebook(gradebook, *, user=None, request=None):
    previous = _gradebook_snapshot(gradebook)
    gradebook.status = GradebookStatus.OPEN
    gradebook.save()
    log_event(
        action="gradebook_opened",
        module="grading",
        user=user,
        model_name=Gradebook.__name__,
        object_id=gradebook.pk,
        previous_data=previous,
        new_data=_gradebook_snapshot(gradebook),
        request=request,
    )
    return gradebook


@transaction.atomic
def close_gradebook(gradebook, *, user=None, request=None):
    previous = _gradebook_snapshot(gradebook)
    gradebook.status = GradebookStatus.CLOSED
    gradebook.save()
    log_event(
        action="gradebook_closed",
        module="grading",
        user=user,
        model_name=Gradebook.__name__,
        object_id=gradebook.pk,
        previous_data=previous,
        new_data=_gradebook_snapshot(gradebook),
        request=request,
    )
    return gradebook


@transaction.atomic
def reopen_gradebook(gradebook, *, reason, user=None, request=None):
    if not reason.strip():
        raise ValidationError({"reason": "La justificacion es obligatoria."})
    previous = _gradebook_snapshot(gradebook)
    gradebook.status = GradebookStatus.REOPENED
    gradebook.save()
    log_event(
        action="gradebook_reopened",
        module="grading",
        user=user,
        model_name=Gradebook.__name__,
        object_id=gradebook.pk,
        previous_data=previous,
        new_data=_gradebook_snapshot(gradebook),
        reason=reason,
        request=request,
    )
    return gradebook


def _record_snapshot(record):
    if record is None:
        return {}
    return {
        "id": record.pk,
        "gradebook_id": record.gradebook_id,
        "course_enrollment_id": record.course_enrollment_id,
        "grade_item_id": record.grade_item_id,
        "score": str(record.score),
        "status": record.status,
        "reason": record.reason,
    }


def _ensure_gradebook_editable(gradebook, *, reason="", allow_closed=False):
    if gradebook.status == GradebookStatus.CLOSED and not allow_closed:
        raise ValidationError({"gradebook": "No se puede modificar un libro cerrado."})
    if (
        gradebook.status == GradebookStatus.CLOSED
        and allow_closed
        and not reason.strip()
    ):
        raise ValidationError(
            {"reason": "La correccion de notas cerradas requiere justificacion."}
        )


@transaction.atomic
def save_grade_record(
    *,
    gradebook,
    course_enrollment,
    grade_item,
    score,
    user=None,
    reason="",
    request=None,
    allow_closed=False,
):
    _ensure_gradebook_editable(gradebook, reason=reason, allow_closed=allow_closed)
    score = validate_score(score)
    record = (
        StudentGradeRecord.objects.filter(
            gradebook=gradebook,
            course_enrollment=course_enrollment,
            grade_item=grade_item,
            status=GradeRecordStatus.ACTIVE,
        )
        .select_for_update()
        .first()
    )
    previous = _record_snapshot(record)
    created = record is None
    if record is None:
        record = StudentGradeRecord(
            gradebook=gradebook,
            course_enrollment=course_enrollment,
            grade_item=grade_item,
            entered_by=user,
        )
    else:
        record.updated_by = user
    record.score = score
    record.reason = reason
    record.save()
    GradeCalculationSnapshot.objects.filter(
        gradebook=gradebook,
        course_enrollment=course_enrollment,
        is_current=True,
    ).update(is_current=False)
    log_event(
        action="grade_record_created" if created else "grade_record_updated",
        module="grading",
        user=user,
        model_name=StudentGradeRecord.__name__,
        object_id=record.pk,
        previous_data=previous,
        new_data=_record_snapshot(record),
        reason=reason,
        request=request,
    )
    return record


@transaction.atomic
def delete_grade_record(
    record, *, user=None, reason="", request=None, allow_closed=False
):
    _ensure_gradebook_editable(
        record.gradebook, reason=reason, allow_closed=allow_closed
    )
    previous = _record_snapshot(record)
    record.status = GradeRecordStatus.DELETED
    record.updated_by = user
    record.reason = reason
    record.save()
    GradeCalculationSnapshot.objects.filter(
        gradebook=record.gradebook,
        course_enrollment=record.course_enrollment,
        is_current=True,
    ).update(is_current=False)
    log_event(
        action="grade_record_deleted",
        module="grading",
        user=user,
        model_name=StudentGradeRecord.__name__,
        object_id=record.pk,
        previous_data=previous,
        new_data=_record_snapshot(record),
        reason=reason,
        request=request,
    )
    return record


def _active_record_map(gradebook, course_enrollment):
    return {
        record.grade_item_id: record.score
        for record in StudentGradeRecord.objects.filter(
            gradebook=gradebook,
            course_enrollment=course_enrollment,
            status=GradeRecordStatus.ACTIVE,
        )
    }


def _children_by_parent(gradebook):
    children = {}
    for item in GradeItem.objects.filter(gradebook=gradebook).order_by("order"):
        children.setdefault(item.parent_id, []).append(item)
    return children


def _s1_s2_input_from_records(gradebook, course_enrollment):
    records = _active_record_map(gradebook, course_enrollment)
    children = _children_by_parent(gradebook)
    learning_outcomes = []
    for outcome in children.get(None, []):
        if outcome.item_type != GradeItemType.LEARNING_OUTCOME:
            continue
        criteria = []
        recovery_score = None
        for item in children.get(outcome.pk, []):
            if item.item_type == GradeItemType.RECOVERY:
                recovery_score = records.get(item.pk)
                continue
            if item.item_type != GradeItemType.CRITERION:
                continue
            activities = [
                {"score": records[activity.pk]}
                for activity in children.get(item.pk, [])
                if activity.pk in records
                and activity.item_type == GradeItemType.ACTIVITY
            ]
            criterion = {"weight": item.weight}
            if activities:
                criterion["activities"] = activities
            elif item.pk in records:
                criterion["score"] = records[item.pk]
            criteria.append(criterion)
        learning_outcomes.append(
            {
                "order": outcome.order,
                "criteria": criteria,
                "recovery_score": recovery_score,
            }
        )
    return learning_outcomes


def _s3_input_from_records(gradebook, course_enrollment):
    records = _active_record_map(gradebook, course_enrollment)
    children = _children_by_parent(gradebook)
    partials = []
    final_evaluation_score = None
    for item in children.get(None, []):
        if item.item_type == GradeItemType.FINAL_EVALUATION:
            final_evaluation_score = records.get(item.pk)
            continue
        if item.item_type != GradeItemType.PARTIAL:
            continue
        practice_activities = []
        evaluation_score = None
        for child in children.get(item.pk, []):
            if (
                child.item_type == GradeItemType.PRACTICE_ACTIVITY
                and child.pk in records
            ):
                practice_activities.append(
                    {"weight": child.weight, "score": records[child.pk]}
                )
            elif child.item_type == GradeItemType.EVALUATION:
                evaluation_score = records.get(child.pk)
        if evaluation_score is None:
            raise ValidationError({"evaluation": "El parcial no tiene evaluacion."})
        partials.append(
            {
                "order": item.order,
                "practice_activities": practice_activities,
                "evaluation_score": evaluation_score,
            }
        )
    return partials, final_evaluation_score


def calculate_gradebook_student(gradebook, course_enrollment):
    config = gradebook.course_section.grading_system.config or {}
    config.setdefault("passing_score", PASSING_SCORE)
    if gradebook.grading_model == GradingModel.S1:
        return calculate_s1_grade(
            _s1_s2_input_from_records(gradebook, course_enrollment),
            config=config,
        )
    if gradebook.grading_model == GradingModel.S2:
        return calculate_s2_grade(
            _s1_s2_input_from_records(gradebook, course_enrollment),
            config=config,
        )
    if gradebook.grading_model == GradingModel.S3:
        partials, final_evaluation = _s3_input_from_records(
            gradebook, course_enrollment
        )
        return calculate_s3_grade(
            partials,
            final_evaluation_score=final_evaluation,
            config=config,
        )
    raise ValidationError({"grading_model": "Modelo de calificacion no soportado."})


@transaction.atomic
def recalculate_gradebook(
    gradebook,
    *,
    course_enrollments=None,
    user=None,
    source="manual_recalculation",
    request=None,
):
    enrollments = (
        course_enrollments or gradebook.course_section.course_enrollments.all()
    )
    snapshots = []
    for course_enrollment in enrollments:
        result = calculate_gradebook_student(gradebook, course_enrollment)
        GradeCalculationSnapshot.objects.filter(
            gradebook=gradebook,
            course_enrollment=course_enrollment,
            is_current=True,
        ).update(is_current=False)
        snapshot = GradeCalculationSnapshot.objects.create(
            gradebook=gradebook,
            course_enrollment=course_enrollment,
            grading_model=gradebook.grading_model,
            final_score=result["final_score"],
            final_letter=result["final_letter"],
            final_status=result["final_status"],
            failed_learning_outcomes_count=result["failed_learning_outcomes_count"],
            recovery_required=result["recovery_required"],
            payload=_json_ready(result),
            rule_version=gradebook.rule_version or RULE_VERSION,
            source=source,
            calculated_by=user,
        )
        snapshots.append(snapshot)
    log_event(
        action="gradebook_recalculated",
        module="grading",
        user=user,
        model_name=Gradebook.__name__,
        object_id=gradebook.pk,
        new_data={"snapshot_count": len(snapshots), "source": source},
        request=request,
    )
    return snapshots


def _json_ready(value):
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    return value
