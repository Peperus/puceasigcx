from decimal import Decimal
from pathlib import Path
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify

from apps.core.models import TimeStampedModel
from apps.enrollment.models import CourseSection, TeachingAssignment, TeachingRole
from apps.teachers.models import Teacher


class SyllabusVersion(models.TextChoices):
    NEW = "new", "Nueva version"
    LEGACY = "legacy", "Version anterior"


class SyllabusStatus(models.TextChoices):
    DRAFT = "draft", "Borrador"
    IN_REVIEW = "in_review", "En revision"
    APPROVED = "approved", "Aprobado"
    OBSERVED = "observed", "Observado"
    FINALIZED = "finalized", "Finalizado"
    ARCHIVED = "archived", "Archivado"


class CompetencyType(models.TextChoices):
    TRANSVERSAL = "transversal", "Transversal"
    DISCIPLINARY = "disciplinary", "Disciplinar"


class LearningOutcomeType(models.TextChoices):
    CAREER = "career", "Carrera"
    SUBJECT = "subject", "Asignatura"


class AchievementLevelCode(models.TextChoices):
    A = "A", "A"
    B = "B", "B"
    C = "C", "C"
    D = "D", "D"


class BibliographyType(models.TextChoices):
    BASIC = "basic", "Basica"
    COMPLEMENTARY = "complementary", "Complementaria"
    RECOMMENDED = "recommended", "Recomendada"
    DIGITAL = "digital", "Digital"


def syllabus_signed_file_path(instance, filename):
    suffix = Path(filename).suffix.lower() or ".pdf"
    course_label = slugify(str(instance.course_section_id or "curso"))
    return f"syllabi/signed/{course_label}/{uuid4().hex}{suffix}"


class Syllabus(TimeStampedModel):
    course_section = models.ForeignKey(
        CourseSection,
        on_delete=models.PROTECT,
        related_name="syllabi",
        verbose_name="curso/paralelo",
    )
    version = models.CharField(
        "version",
        max_length=20,
        choices=SyllabusVersion.choices,
        default=SyllabusVersion.NEW,
    )
    status = models.CharField(
        "estado",
        max_length=20,
        choices=SyllabusStatus.choices,
        default=SyllabusStatus.DRAFT,
    )
    subject_description = models.TextField("descripcion de la asignatura", blank=True)
    methodology = models.TextField("metodologia", blank=True)
    lead_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        related_name="lead_syllabi",
        verbose_name="docente titular",
    )
    co_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        related_name="co_taught_syllabi",
        null=True,
        blank=True,
        verbose_name="codocente",
    )
    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        related_name="created_syllabi",
        null=True,
        blank=True,
        verbose_name="creado por",
    )
    finalized_at = models.DateTimeField("fecha de finalizacion", null=True, blank=True)
    submitted_at = models.DateTimeField("fecha de envio", null=True, blank=True)
    approved_at = models.DateTimeField("fecha de aprobacion", null=True, blank=True)
    approved_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        related_name="approved_syllabi",
        null=True,
        blank=True,
        verbose_name="aprobado por",
    )
    signed_file = models.FileField(
        "silabo firmado",
        upload_to=syllabus_signed_file_path,
        validators=[FileExtensionValidator(["pdf"])],
        blank=True,
    )
    signed_file_uploaded_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        related_name="uploaded_signed_syllabi",
        null=True,
        blank=True,
        verbose_name="archivo subido por",
    )
    signed_file_uploaded_at = models.DateTimeField(
        "fecha de carga de archivo",
        null=True,
        blank=True,
    )
    archived_at = models.DateTimeField("fecha de archivo", null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "course_section__subject__code"]
        verbose_name = "silabo"
        verbose_name_plural = "silabos"
        constraints = [
            models.UniqueConstraint(
                fields=["course_section"],
                condition=~Q(status=SyllabusStatus.ARCHIVED),
                name="unique_active_syllabus_per_course_section",
            )
        ]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["version"]),
        ]

    def __str__(self):
        return f"Silabo {self.course_section} ({self.get_status_display()})"

    @property
    def is_editable(self):
        return self.status in {SyllabusStatus.DRAFT, SyllabusStatus.OBSERVED}

    @property
    def is_ready_for_grading(self):
        return self.status == SyllabusStatus.APPROVED

    def clean(self):
        errors = {}
        if self.co_teacher_id and self.co_teacher_id == self.lead_teacher_id:
            errors["co_teacher"] = "El codocente debe ser distinto del titular."
        if self.course_section_id and self.lead_teacher_id:
            lead_exists = TeachingAssignment.objects.filter(
                course_section_id=self.course_section_id,
                teacher_id=self.lead_teacher_id,
                role=TeachingRole.LEAD,
            ).exists()
            if not lead_exists:
                errors["lead_teacher"] = (
                    "El docente titular debe estar asignado como titular del curso."
                )
        if self.course_section_id and self.co_teacher_id:
            co_teacher_exists = TeachingAssignment.objects.filter(
                course_section_id=self.course_section_id,
                teacher_id=self.co_teacher_id,
                role=TeachingRole.CO_TEACHER,
            ).exists()
            if not co_teacher_exists:
                errors["co_teacher"] = (
                    "El codocente debe estar asignado como codocente del curso."
                )
        if self.status == SyllabusStatus.APPROVED and not self.approved_at:
            self.approved_at = timezone.now()
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SyllabusChildModel(TimeStampedModel):
    syllabus = models.ForeignKey(
        Syllabus,
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        verbose_name="silabo",
    )

    class Meta:
        abstract = True

    def clean(self):
        if self.syllabus_id and not self.syllabus.is_editable:
            raise ValidationError(
                {"syllabus": "Solo se puede editar un silabo en borrador u observado."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SyllabusCompetency(SyllabusChildModel):
    competency_type = models.CharField(
        "tipo",
        max_length=20,
        choices=CompetencyType.choices,
    )
    text = models.TextField("competencia")
    order = models.PositiveSmallIntegerField("orden", default=1)

    class Meta:
        ordering = ["syllabus", "competency_type", "order"]
        verbose_name = "competencia de silabo"
        verbose_name_plural = "competencias de silabo"
        constraints = [
            models.UniqueConstraint(
                fields=["syllabus", "competency_type", "order"],
                name="unique_syllabus_competency_order",
            )
        ]

    def __str__(self):
        return f"{self.get_competency_type_display()} {self.order}"


class SyllabusLearningOutcome(SyllabusChildModel):
    outcome_type = models.CharField(
        "tipo",
        max_length=20,
        choices=LearningOutcomeType.choices,
    )
    code = models.CharField("codigo", max_length=30, blank=True)
    text = models.TextField("resultado de aprendizaje")
    order = models.PositiveSmallIntegerField("orden", default=1)

    class Meta:
        ordering = ["syllabus", "outcome_type", "order"]
        verbose_name = "resultado de aprendizaje de silabo"
        verbose_name_plural = "resultados de aprendizaje de silabo"
        constraints = [
            models.UniqueConstraint(
                fields=["syllabus", "outcome_type", "order"],
                name="unique_syllabus_learning_outcome_order",
            )
        ]

    def __str__(self):
        return f"{self.get_outcome_type_display()} {self.order}"


class SyllabusCriterion(SyllabusChildModel):
    learning_outcome = models.ForeignKey(
        SyllabusLearningOutcome,
        on_delete=models.CASCADE,
        related_name="criteria",
        verbose_name="resultado de aprendizaje",
    )
    name = models.CharField("nombre", max_length=160)
    description = models.TextField("descripcion", blank=True)
    weight = models.DecimalField(
        "ponderacion",
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01")),
            MaxValueValidator(Decimal("100.00")),
        ],
    )
    order = models.PositiveSmallIntegerField("orden", default=1)

    class Meta:
        ordering = ["learning_outcome", "order"]
        verbose_name = "criterio de evaluacion de silabo"
        verbose_name_plural = "criterios de evaluacion de silabo"
        constraints = [
            models.UniqueConstraint(
                fields=["learning_outcome", "order"],
                name="unique_syllabus_criterion_order",
            )
        ]

    def clean(self):
        super().clean()
        if (
            self.syllabus_id
            and self.learning_outcome_id
            and self.learning_outcome.syllabus_id != self.syllabus_id
        ):
            raise ValidationError(
                {
                    "learning_outcome": (
                        "El resultado de aprendizaje debe pertenecer al mismo silabo."
                    )
                }
            )

    def __str__(self):
        return f"{self.learning_outcome} - {self.name}"


class SyllabusAchievementLevel(TimeStampedModel):
    criterion = models.ForeignKey(
        SyllabusCriterion,
        on_delete=models.CASCADE,
        related_name="achievement_levels",
        verbose_name="criterio",
    )
    level = models.CharField(
        "nivel", max_length=1, choices=AchievementLevelCode.choices
    )
    description = models.TextField("descripcion")

    class Meta:
        ordering = ["criterion", "level"]
        verbose_name = "nivel de logro de silabo"
        verbose_name_plural = "niveles de logro de silabo"
        constraints = [
            models.UniqueConstraint(
                fields=["criterion", "level"],
                name="unique_syllabus_achievement_level",
            )
        ]

    def clean(self):
        if self.criterion_id and not self.criterion.syllabus.is_editable:
            raise ValidationError(
                {"criterion": "Solo se puede editar un silabo en borrador u observado."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.criterion} - {self.level}"


class SyllabusBibliography(SyllabusChildModel):
    bibliography_type = models.CharField(
        "tipo",
        max_length=20,
        choices=BibliographyType.choices,
    )
    apa_reference = models.TextField("referencia APA")
    library_code = models.CharField("codigo biblioteca", max_length=80, blank=True)
    copies = models.PositiveSmallIntegerField(
        "cantidad de ejemplares",
        default=0,
    )
    order = models.PositiveSmallIntegerField("orden", default=1)

    class Meta:
        ordering = ["syllabus", "bibliography_type", "order"]
        verbose_name = "bibliografia de silabo"
        verbose_name_plural = "bibliografias de silabo"

    def __str__(self):
        return f"{self.get_bibliography_type_display()} {self.order}"


class SyllabusWeeklyPlan(SyllabusChildModel):
    learning_outcome = models.ForeignKey(
        SyllabusLearningOutcome,
        on_delete=models.PROTECT,
        related_name="weekly_plans",
        verbose_name="resultado de aprendizaje",
    )
    week_number = models.PositiveSmallIntegerField("semana")
    week_label = models.CharField("etiqueta", max_length=80, blank=True)
    start_date = models.DateField("fecha inicio", null=True, blank=True)
    end_date = models.DateField("fecha fin", null=True, blank=True)
    knowledge_dimension = models.CharField("dimension del conocimiento", max_length=160)
    contact_strategy = models.TextField("experiencia contacto docente", blank=True)
    contact_hours = models.DecimalField(
        "horas contacto docente",
        max_digits=6,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    contact_resources = models.TextField("recursos contacto", blank=True)
    contact_scenarios = models.TextField("escenarios contacto", blank=True)
    practical_strategy = models.TextField(
        "experiencia practico-experimental", blank=True
    )
    practical_hours = models.DecimalField(
        "horas practico-experimentales",
        max_digits=6,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    practical_resources = models.TextField("recursos practicos", blank=True)
    practical_scenarios = models.TextField("escenarios practicos", blank=True)
    autonomous_strategy = models.TextField("experiencia autonoma", blank=True)
    autonomous_hours = models.DecimalField(
        "horas autonomas",
        max_digits=6,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    autonomous_resources = models.TextField("recursos autonomos", blank=True)
    autonomous_scenarios = models.TextField("escenarios autonomos", blank=True)

    class Meta:
        ordering = ["syllabus", "week_number"]
        verbose_name = "planificacion semanal de silabo"
        verbose_name_plural = "planificaciones semanales de silabo"
        constraints = [
            models.UniqueConstraint(
                fields=["syllabus", "week_number"],
                name="unique_syllabus_week_number",
            )
        ]

    def clean(self):
        super().clean()
        errors = {}
        if (
            self.syllabus_id
            and self.learning_outcome_id
            and self.learning_outcome.syllabus_id != self.syllabus_id
        ):
            errors["learning_outcome"] = (
                "El resultado de aprendizaje debe pertenecer al mismo silabo."
            )
        if self.start_date and self.end_date and self.start_date > self.end_date:
            errors["end_date"] = "La fecha final no puede ser anterior a la inicial."
        if not any(
            [
                self.contact_strategy.strip(),
                self.practical_strategy.strip(),
                self.autonomous_strategy.strip(),
            ]
        ):
            errors["contact_strategy"] = (
                "Registre al menos una experiencia de aprendizaje."
            )
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.week_label or f"Semana {self.week_number}"
