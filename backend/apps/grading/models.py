from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone

from apps.core.models import TimeStampedModel
from apps.enrollment.models import (
    CourseEnrollment,
    CourseEnrollmentStatus,
    CourseSection,
    CourseSectionStatus,
)
from apps.syllabus.models import Syllabus


class GradingModel(models.TextChoices):
    S1 = "S1", "S1"
    S2 = "S2", "S2"
    S3 = "S3", "S3"


class GradebookStatus(models.TextChoices):
    DRAFT = "draft", "Borrador"
    OPEN = "open", "Abierto"
    SUBMITTED = "submitted", "Enviado"
    CLOSED = "closed", "Cerrado"
    REOPENED = "reopened", "Reabierto"
    ARCHIVED = "archived", "Archivado"


class GradeItemType(models.TextChoices):
    LEARNING_OUTCOME = "learning_outcome", "Resultado de aprendizaje"
    CRITERION = "criterion", "Criterio"
    ACTIVITY = "activity", "Actividad"
    RECOVERY = "recovery", "Recuperacion"
    PARTIAL = "partial", "Parcial"
    PRACTICE_ACTIVITY = "practice_activity", "Actividad practica"
    EVALUATION = "evaluation", "Evaluacion"
    FINAL_EVALUATION = "final_evaluation", "Evaluacion final"


class GradeRecordStatus(models.TextChoices):
    ACTIVE = "active", "Activo"
    DELETED = "deleted", "Eliminado logicamente"


class GradeFinalStatus(models.TextChoices):
    PENDING = "pending", "Pendiente"
    APPROVED = "approved", "Aprobado"
    RECOVERY_REQUIRED = "recovery_required", "Recuperacion requerida"
    INTERSEMESTRAL = "intersemestral", "Intersemestral"
    FAILED = "failed", "Reprobado"


class Gradebook(TimeStampedModel):
    course_section = models.OneToOneField(
        CourseSection,
        on_delete=models.PROTECT,
        related_name="gradebook",
        verbose_name="curso/paralelo",
    )
    syllabus = models.ForeignKey(
        Syllabus,
        on_delete=models.PROTECT,
        related_name="gradebooks",
        verbose_name="silabo",
    )
    grading_model = models.CharField(
        "modelo de calificacion",
        max_length=2,
        choices=GradingModel.choices,
        blank=True,
    )
    status = models.CharField(
        "estado",
        max_length=20,
        choices=GradebookStatus.choices,
        default=GradebookStatus.DRAFT,
    )
    opened_at = models.DateTimeField("fecha de apertura", null=True, blank=True)
    closed_at = models.DateTimeField("fecha de cierre", null=True, blank=True)
    reopened_at = models.DateTimeField("fecha de reapertura", null=True, blank=True)
    rule_version = models.CharField("version de reglas", max_length=40, default="S6.1")

    class Meta:
        ordering = ["course_section__offer__period__code", "course_section"]
        verbose_name = "libro de calificaciones"
        verbose_name_plural = "libros de calificaciones"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["grading_model"]),
        ]

    def __str__(self):
        return f"{self.course_section} - {self.grading_model or 'sin modelo'}"

    def clean(self):
        errors = {}
        if self.course_section_id:
            if self.course_section.status != CourseSectionStatus.ACTIVE:
                errors["course_section"] = (
                    "Solo se puede crear un libro para cursos activos."
                )
            inherited_model = self.course_section.grading_system.code.upper()
            if inherited_model not in GradingModel.values:
                errors["grading_model"] = (
                    "El curso debe usar un sistema de calificacion S1, S2 o S3."
                )
            elif self.grading_model and self.grading_model != inherited_model:
                errors["grading_model"] = (
                    "El modelo debe coincidir con el sistema configurado en el curso."
                )
        if self.syllabus_id:
            if (
                self.course_section_id
                and self.syllabus.course_section_id != self.course_section_id
            ):
                errors["syllabus"] = (
                    "El silabo debe pertenecer al mismo curso/paralelo."
                )
            if not self.syllabus.is_ready_for_grading:
                errors["syllabus"] = (
                    "El silabo debe estar aprobado antes de abrir calificaciones."
                )
        if self.status in {GradebookStatus.OPEN, GradebookStatus.REOPENED}:
            self.opened_at = self.opened_at or timezone.now()
        if self.status == GradebookStatus.CLOSED and not self.closed_at:
            self.closed_at = timezone.now()
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.course_section_id and not self.grading_model:
            self.grading_model = self.course_section.grading_system.code.upper()
        self.full_clean()
        super().save(*args, **kwargs)


class GradeItem(TimeStampedModel):
    gradebook = models.ForeignKey(
        Gradebook,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="libro de calificaciones",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
        verbose_name="item padre",
    )
    item_type = models.CharField("tipo", max_length=30, choices=GradeItemType.choices)
    name = models.CharField("nombre", max_length=160)
    order = models.PositiveSmallIntegerField("orden", default=1)
    weight = models.DecimalField(
        "ponderacion",
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("100.00")),
        ],
    )
    max_score = models.DecimalField(
        "nota maxima",
        max_digits=5,
        decimal_places=2,
        default=Decimal("50.00"),
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    syllabus_learning_outcome = models.ForeignKey(
        "syllabus.SyllabusLearningOutcome",
        on_delete=models.PROTECT,
        related_name="grade_items",
        null=True,
        blank=True,
        verbose_name="resultado de aprendizaje del silabo",
    )
    syllabus_criterion = models.ForeignKey(
        "syllabus.SyllabusCriterion",
        on_delete=models.PROTECT,
        related_name="grade_items",
        null=True,
        blank=True,
        verbose_name="criterio del silabo",
    )

    class Meta:
        ordering = ["gradebook", "parent_id", "order"]
        verbose_name = "item de calificacion"
        verbose_name_plural = "items de calificacion"
        constraints = [
            models.UniqueConstraint(
                fields=["gradebook", "parent", "item_type", "order"],
                name="unique_grade_item_order_per_parent_type",
            )
        ]

    def __str__(self):
        return f"{self.gradebook} - {self.name}"

    def clean(self):
        errors = {}
        if self.parent_id and self.parent.gradebook_id != self.gradebook_id:
            errors["parent"] = "El item padre debe pertenecer al mismo libro."
        if (
            self.syllabus_learning_outcome_id
            and self.gradebook_id
            and self.syllabus_learning_outcome.syllabus_id != self.gradebook.syllabus_id
        ):
            errors["syllabus_learning_outcome"] = (
                "El resultado de aprendizaje debe pertenecer al silabo del libro."
            )
        if (
            self.syllabus_criterion_id
            and self.gradebook_id
            and self.syllabus_criterion.syllabus_id != self.gradebook.syllabus_id
        ):
            errors["syllabus_criterion"] = (
                "El criterio debe pertenecer al silabo del libro."
            )
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class StudentGradeRecord(TimeStampedModel):
    gradebook = models.ForeignKey(
        Gradebook,
        on_delete=models.CASCADE,
        related_name="grade_records",
        verbose_name="libro de calificaciones",
    )
    course_enrollment = models.ForeignKey(
        CourseEnrollment,
        on_delete=models.PROTECT,
        related_name="grade_records",
        verbose_name="matricula en curso",
    )
    grade_item = models.ForeignKey(
        GradeItem,
        on_delete=models.PROTECT,
        related_name="student_records",
        verbose_name="item de calificacion",
    )
    score = models.DecimalField(
        "nota",
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("50.00")),
        ],
    )
    status = models.CharField(
        "estado",
        max_length=20,
        choices=GradeRecordStatus.choices,
        default=GradeRecordStatus.ACTIVE,
    )
    entered_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        related_name="entered_grade_records",
        null=True,
        blank=True,
        verbose_name="ingresado por",
    )
    updated_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        related_name="updated_grade_records",
        null=True,
        blank=True,
        verbose_name="actualizado por",
    )
    reason = models.TextField("justificacion", blank=True)

    class Meta:
        ordering = ["gradebook", "course_enrollment", "grade_item__order"]
        verbose_name = "registro de nota"
        verbose_name_plural = "registros de notas"
        constraints = [
            models.UniqueConstraint(
                fields=["gradebook", "course_enrollment", "grade_item"],
                condition=Q(status=GradeRecordStatus.ACTIVE),
                name="unique_active_grade_record_per_student_item",
            )
        ]
        indexes = [
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.course_enrollment} - {self.grade_item}: {self.score}"

    def clean(self):
        errors = {}
        if self.grade_item_id and self.grade_item.gradebook_id != self.gradebook_id:
            errors["grade_item"] = "El item debe pertenecer al libro indicado."
        if (
            self.course_enrollment_id
            and self.gradebook_id
            and self.course_enrollment.course_section_id
            != self.gradebook.course_section_id
        ):
            errors["course_enrollment"] = (
                "La matricula debe pertenecer al curso del libro."
            )
        if (
            self.course_enrollment_id
            and self.status == GradeRecordStatus.ACTIVE
            and self.course_enrollment.status != CourseEnrollmentStatus.ENROLLED
        ):
            errors["course_enrollment"] = (
                "Solo se registran notas para matriculas activas."
            )
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class GradeCalculationSnapshot(models.Model):
    gradebook = models.ForeignKey(
        Gradebook,
        on_delete=models.CASCADE,
        related_name="calculation_snapshots",
        verbose_name="libro de calificaciones",
    )
    course_enrollment = models.ForeignKey(
        CourseEnrollment,
        on_delete=models.PROTECT,
        related_name="grade_snapshots",
        verbose_name="matricula en curso",
    )
    grading_model = models.CharField(
        "modelo",
        max_length=2,
        choices=GradingModel.choices,
    )
    final_score = models.DecimalField("nota final", max_digits=5, decimal_places=2)
    final_letter = models.CharField("letra final", max_length=1)
    final_status = models.CharField(
        "estado final",
        max_length=30,
        choices=GradeFinalStatus.choices,
    )
    failed_learning_outcomes_count = models.PositiveSmallIntegerField(
        "resultados no alcanzados",
        default=0,
    )
    recovery_required = models.BooleanField("requiere recuperacion", default=False)
    payload = models.JSONField("detalle calculado", default=dict)
    rule_version = models.CharField("version de regla", max_length=40)
    source = models.CharField("fuente", max_length=60, default="manual_recalculation")
    calculated_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        related_name="grade_calculations",
        null=True,
        blank=True,
        verbose_name="calculado por",
    )
    calculated_at = models.DateTimeField("fecha de calculo", default=timezone.now)
    is_current = models.BooleanField("snapshot vigente", default=True)

    class Meta:
        ordering = ["-calculated_at"]
        verbose_name = "snapshot de calculo de nota"
        verbose_name_plural = "snapshots de calculo de notas"
        constraints = [
            models.UniqueConstraint(
                fields=["gradebook", "course_enrollment"],
                condition=Q(is_current=True),
                name="unique_current_grade_snapshot_per_student",
            )
        ]
        indexes = [
            models.Index(fields=["grading_model", "final_status"]),
            models.Index(fields=["calculated_at"]),
        ]

    def __str__(self):
        return f"{self.course_enrollment} - {self.final_score} ({self.final_status})"
