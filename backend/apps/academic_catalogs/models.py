from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from apps.core.models import TimeStampedModel


class PeriodStatus(models.TextChoices):
    DRAFT = "draft", "Borrador"
    ACTIVE = "active", "Activo"
    CLOSED = "closed", "Cerrado"
    ARCHIVED = "archived", "Archivado"


class CatalogStatus(models.TextChoices):
    ACTIVE = "active", "Activo"
    INACTIVE = "inactive", "Inactivo"
    ARCHIVED = "archived", "Archivado"


class SyllabusVersion(models.TextChoices):
    NEW = "new", "Nueva version"
    LEGACY = "legacy", "Version anterior"


class AcademicPeriod(TimeStampedModel):
    name = models.CharField("nombre", max_length=150)
    code = models.CharField("codigo", max_length=30, unique=True)
    start_date = models.DateField("fecha de inicio")
    end_date = models.DateField("fecha de fin")
    enrollment_start_date = models.DateField("inicio de matricula")
    enrollment_end_date = models.DateField("fin de matricula")
    status = models.CharField(
        "estado",
        max_length=20,
        choices=PeriodStatus.choices,
        default=PeriodStatus.DRAFT,
    )
    is_current = models.BooleanField("periodo actual", default=False)

    class Meta:
        ordering = ["-start_date", "code"]
        verbose_name = "periodo academico"
        verbose_name_plural = "periodos academicos"
        constraints = [
            models.UniqueConstraint(
                fields=["is_current"],
                condition=Q(is_current=True),
                name="unique_current_academic_period",
            ),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def clean(self):
        errors = {}
        if self.start_date and self.end_date and self.start_date > self.end_date:
            errors["end_date"] = "La fecha de fin debe ser posterior al inicio."

        if (
            self.enrollment_start_date
            and self.enrollment_end_date
            and self.enrollment_start_date > self.enrollment_end_date
        ):
            errors["enrollment_end_date"] = (
                "La fecha de fin de matricula debe ser posterior al inicio."
            )

        if (
            self.start_date
            and self.end_date
            and self.enrollment_start_date
            and self.enrollment_end_date
            and (
                self.enrollment_start_date < self.start_date
                or self.enrollment_end_date > self.end_date
            )
        ):
            errors["enrollment_start_date"] = (
                "Las fechas de matricula deben estar dentro del periodo."
            )

        if self.status == PeriodStatus.ACTIVE and self.start_date and self.end_date:
            overlapping_periods = AcademicPeriod.objects.filter(
                status=PeriodStatus.ACTIVE,
                start_date__lte=self.end_date,
                end_date__gte=self.start_date,
            )
            if self.pk:
                overlapping_periods = overlapping_periods.exclude(pk=self.pk)
            if overlapping_periods.exists():
                errors["status"] = (
                    "No puede existir otro periodo activo con fechas solapadas."
                )

        if self.is_current:
            current_periods = AcademicPeriod.objects.filter(is_current=True)
            if self.pk:
                current_periods = current_periods.exclude(pk=self.pk)
            if current_periods.exists():
                errors["is_current"] = "Ya existe un periodo marcado como actual."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class FacultyOrUnit(TimeStampedModel):
    code = models.CharField("codigo", max_length=30, unique=True)
    name = models.CharField("nombre", max_length=150)
    description = models.TextField("descripcion", blank=True)
    status = models.CharField(
        "estado",
        max_length=20,
        choices=CatalogStatus.choices,
        default=CatalogStatus.ACTIVE,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "unidad academica"
        verbose_name_plural = "unidades academicas"

    def __str__(self):
        return self.name


class Modality(TimeStampedModel):
    code = models.CharField("codigo", max_length=30, unique=True)
    name = models.CharField("nombre", max_length=100)
    description = models.TextField("descripcion", blank=True)
    status = models.CharField(
        "estado",
        max_length=20,
        choices=CatalogStatus.choices,
        default=CatalogStatus.ACTIVE,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "modalidad"
        verbose_name_plural = "modalidades"

    def __str__(self):
        return self.name


class AcademicDomain(TimeStampedModel):
    code = models.CharField("codigo", max_length=30, unique=True)
    name = models.CharField("nombre", max_length=150)
    description = models.TextField("descripcion", blank=True)
    status = models.CharField(
        "estado",
        max_length=20,
        choices=CatalogStatus.choices,
        default=CatalogStatus.ACTIVE,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "dominio academico"
        verbose_name_plural = "dominios academicos"

    def __str__(self):
        return self.name


class Career(TimeStampedModel):
    code = models.CharField("codigo", max_length=30, unique=True)
    name = models.CharField("nombre", max_length=150)
    faculty = models.ForeignKey(
        FacultyOrUnit,
        on_delete=models.PROTECT,
        related_name="careers",
        null=True,
        blank=True,
        verbose_name="unidad academica",
    )
    modality = models.ForeignKey(
        Modality,
        on_delete=models.PROTECT,
        related_name="careers",
        verbose_name="modalidad",
    )
    domain = models.ForeignKey(
        AcademicDomain,
        on_delete=models.PROTECT,
        related_name="careers",
        null=True,
        blank=True,
        verbose_name="dominio",
    )
    coordinator_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="coordinated_careers",
        null=True,
        blank=True,
        verbose_name="coordinador",
    )
    description = models.TextField("descripcion", blank=True)
    status = models.CharField(
        "estado",
        max_length=20,
        choices=CatalogStatus.choices,
        default=CatalogStatus.ACTIVE,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "carrera"
        verbose_name_plural = "carreras"

    def __str__(self):
        return self.name


class StudyPlan(TimeStampedModel):
    career = models.ForeignKey(
        Career,
        on_delete=models.PROTECT,
        related_name="study_plans",
        verbose_name="carrera",
    )
    code = models.CharField("codigo", max_length=30)
    name = models.CharField("nombre", max_length=150)
    version = models.CharField("version", max_length=40)
    effective_from = models.DateField("vigente desde")
    effective_to = models.DateField("vigente hasta", null=True, blank=True)
    is_current = models.BooleanField("plan vigente", default=False)
    status = models.CharField(
        "estado",
        max_length=20,
        choices=CatalogStatus.choices,
        default=CatalogStatus.ACTIVE,
    )

    class Meta:
        ordering = ["career__name", "-effective_from", "code"]
        verbose_name = "plan de estudio"
        verbose_name_plural = "planes de estudio"
        constraints = [
            models.UniqueConstraint(
                fields=["career", "code"],
                name="unique_study_plan_code_per_career",
            ),
            models.UniqueConstraint(
                fields=["career", "is_current"],
                condition=Q(is_current=True),
                name="unique_current_study_plan_per_career",
            ),
        ]

    def __str__(self):
        return f"{self.career.code} - {self.code}"

    def clean(self):
        if (
            self.effective_from
            and self.effective_to
            and self.effective_from > self.effective_to
        ):
            raise ValidationError(
                {"effective_to": "La fecha final debe ser posterior al inicio."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class AcademicLevel(TimeStampedModel):
    study_plan = models.ForeignKey(
        StudyPlan,
        on_delete=models.CASCADE,
        related_name="levels",
        verbose_name="plan de estudio",
    )
    number = models.PositiveSmallIntegerField(
        "numero", validators=[MinValueValidator(1)]
    )
    name = models.CharField("nombre", max_length=80)
    order = models.PositiveSmallIntegerField("orden", validators=[MinValueValidator(1)])

    class Meta:
        ordering = ["study_plan", "order"]
        verbose_name = "nivel academico"
        verbose_name_plural = "niveles academicos"
        constraints = [
            models.UniqueConstraint(
                fields=["study_plan", "number"],
                name="unique_level_number_per_study_plan",
            ),
            models.UniqueConstraint(
                fields=["study_plan", "order"],
                name="unique_level_order_per_study_plan",
            ),
        ]

    def __str__(self):
        return f"{self.study_plan.code} - Nivel {self.number}"


class GradingSystem(TimeStampedModel):
    code = models.CharField("codigo", max_length=10, unique=True)
    name = models.CharField("nombre", max_length=100)
    description = models.TextField("descripcion", blank=True)
    config = models.JSONField("configuracion", default=dict, blank=True)
    is_active = models.BooleanField("activo", default=True)

    class Meta:
        ordering = ["code"]
        verbose_name = "sistema de calificacion"
        verbose_name_plural = "sistemas de calificacion"

    def __str__(self):
        return self.code


class Subject(TimeStampedModel):
    career = models.ForeignKey(
        Career,
        on_delete=models.PROTECT,
        related_name="subjects",
        verbose_name="carrera",
    )
    code = models.CharField("codigo", max_length=30)
    name = models.CharField("nombre", max_length=180)
    total_hours = models.PositiveSmallIntegerField("horas totales")
    contact_hours = models.PositiveSmallIntegerField("horas contacto docente")
    autonomous_hours = models.PositiveSmallIntegerField("horas autonomas")
    practical_hours = models.PositiveSmallIntegerField("horas practico-experimentales")
    default_syllabus_version = models.CharField(
        "version de silabo por defecto",
        max_length=20,
        choices=SyllabusVersion.choices,
        default=SyllabusVersion.NEW,
    )
    default_grading_system = models.ForeignKey(
        GradingSystem,
        on_delete=models.PROTECT,
        related_name="subjects",
        null=True,
        blank=True,
        verbose_name="sistema de calificacion por defecto",
    )
    description = models.TextField("descripcion", blank=True)
    status = models.CharField(
        "estado",
        max_length=20,
        choices=CatalogStatus.choices,
        default=CatalogStatus.ACTIVE,
    )

    class Meta:
        ordering = ["career__name", "code"]
        verbose_name = "asignatura"
        verbose_name_plural = "asignaturas"
        constraints = [
            models.UniqueConstraint(
                fields=["career", "code"],
                name="unique_subject_code_per_career",
            ),
            models.CheckConstraint(
                condition=Q(
                    total_hours=models.F("contact_hours")
                    + models.F("autonomous_hours")
                    + models.F("practical_hours")
                ),
                name="subject_hours_match_total",
            ),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class CurriculumSubject(TimeStampedModel):
    study_plan = models.ForeignKey(
        StudyPlan,
        on_delete=models.CASCADE,
        related_name="curriculum_subjects",
        verbose_name="plan de estudio",
    )
    level = models.ForeignKey(
        AcademicLevel,
        on_delete=models.PROTECT,
        related_name="curriculum_subjects",
        verbose_name="nivel",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="curriculum_entries",
        verbose_name="asignatura",
    )
    domain = models.ForeignKey(
        AcademicDomain,
        on_delete=models.PROTECT,
        related_name="curriculum_subjects",
        null=True,
        blank=True,
        verbose_name="dominio",
    )
    order = models.PositiveSmallIntegerField("orden", validators=[MinValueValidator(1)])
    credits = models.DecimalField(
        "creditos",
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["study_plan", "level__order", "order", "subject__code"]
        verbose_name = "asignatura de malla"
        verbose_name_plural = "asignaturas de malla"
        constraints = [
            models.UniqueConstraint(
                fields=["study_plan", "subject"],
                name="unique_subject_per_study_plan",
            ),
            models.UniqueConstraint(
                fields=["study_plan", "level", "order"],
                name="unique_curriculum_order_per_level",
            ),
        ]

    def __str__(self):
        return f"{self.study_plan.code} - {self.subject.code}"

    def clean(self):
        errors = {}
        if (
            self.level_id
            and self.study_plan_id
            and self.level.study_plan_id != self.study_plan_id
        ):
            errors["level"] = "El nivel debe pertenecer al plan de estudio."
        if (
            self.subject_id
            and self.study_plan_id
            and self.subject.career_id != self.study_plan.career_id
        ):
            errors["subject"] = "La asignatura debe pertenecer a la carrera del plan."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class CurriculumPrerequisite(TimeStampedModel):
    curriculum_subject = models.ForeignKey(
        CurriculumSubject,
        on_delete=models.CASCADE,
        related_name="prerequisite_links",
        verbose_name="asignatura de malla",
    )
    prerequisite = models.ForeignKey(
        CurriculumSubject,
        on_delete=models.CASCADE,
        related_name="required_by_links",
        verbose_name="prerrequisito",
    )

    class Meta:
        ordering = ["curriculum_subject", "prerequisite"]
        verbose_name = "prerrequisito"
        verbose_name_plural = "prerrequisitos"
        constraints = [
            models.UniqueConstraint(
                fields=["curriculum_subject", "prerequisite"],
                name="unique_curriculum_prerequisite",
            )
        ]

    def __str__(self):
        return f"{self.prerequisite} -> {self.curriculum_subject}"

    def clean(self):
        errors = {}
        if self.curriculum_subject_id == self.prerequisite_id:
            errors["prerequisite"] = (
                "Una asignatura no puede ser prerrequisito de si misma."
            )

        if (
            self.curriculum_subject_id
            and self.prerequisite_id
            and self.curriculum_subject.study_plan_id != self.prerequisite.study_plan_id
        ):
            errors["prerequisite"] = "El prerrequisito debe pertenecer al mismo plan."

        if self.curriculum_subject_id and self.prerequisite_id:
            reverse_exists = CurriculumPrerequisite.objects.filter(
                curriculum_subject=self.prerequisite,
                prerequisite=self.curriculum_subject,
            )
            if self.pk:
                reverse_exists = reverse_exists.exclude(pk=self.pk)
            if reverse_exists.exists():
                errors["prerequisite"] = (
                    "No se permiten ciclos simples de prerrequisitos."
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class AcademicSetting(TimeStampedModel):
    name = models.CharField("nombre", max_length=120)
    period = models.ForeignKey(
        AcademicPeriod,
        on_delete=models.CASCADE,
        related_name="settings",
        null=True,
        blank=True,
        verbose_name="periodo",
    )
    career = models.ForeignKey(
        Career,
        on_delete=models.CASCADE,
        related_name="settings",
        null=True,
        blank=True,
        verbose_name="carrera",
    )
    score_min = models.DecimalField(
        "nota minima",
        max_digits=5,
        decimal_places=2,
        default=0,
    )
    score_max = models.DecimalField(
        "nota maxima",
        max_digits=5,
        decimal_places=2,
        default=50,
    )
    passing_score = models.DecimalField(
        "umbral de aprobacion",
        max_digits=5,
        decimal_places=2,
        default=30,
    )
    default_grading_system = models.ForeignKey(
        GradingSystem,
        on_delete=models.PROTECT,
        related_name="academic_settings",
        null=True,
        blank=True,
        verbose_name="sistema de calificacion por defecto",
    )
    is_default = models.BooleanField("configuracion global por defecto", default=False)

    class Meta:
        ordering = ["-is_default", "career__name", "period__code", "name"]
        verbose_name = "configuracion academica"
        verbose_name_plural = "configuraciones academicas"
        constraints = [
            models.UniqueConstraint(
                fields=["is_default"],
                condition=Q(is_default=True),
                name="unique_default_academic_setting",
            ),
            models.UniqueConstraint(
                fields=["period", "career"],
                condition=Q(period__isnull=False, career__isnull=False),
                name="unique_academic_setting_per_period_career",
            ),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        errors = {}
        if self.score_min >= self.score_max:
            errors["score_max"] = "La nota maxima debe ser mayor que la minima."
        if not self.score_min <= self.passing_score <= self.score_max:
            errors["passing_score"] = (
                "El umbral de aprobacion debe estar dentro de la escala."
            )
        if self.is_default and (self.period_id or self.career_id):
            errors["is_default"] = (
                "La configuracion por defecto no debe asociarse a periodo o carrera."
            )
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class AchievementLevel(TimeStampedModel):
    setting = models.ForeignKey(
        AcademicSetting,
        on_delete=models.CASCADE,
        related_name="achievement_levels",
        verbose_name="configuracion",
    )
    letter = models.CharField("letra", max_length=1)
    min_score = models.DecimalField("nota minima", max_digits=5, decimal_places=2)
    max_score = models.DecimalField("nota maxima", max_digits=5, decimal_places=2)
    description = models.CharField("descripcion", max_length=180)

    class Meta:
        ordering = ["setting", "-min_score"]
        verbose_name = "nivel de logro"
        verbose_name_plural = "niveles de logro"
        constraints = [
            models.UniqueConstraint(
                fields=["setting", "letter"],
                name="unique_achievement_letter_per_setting",
            )
        ]

    def __str__(self):
        return f"{self.letter} ({self.min_score}-{self.max_score})"

    def clean(self):
        errors = {}
        if self.min_score > self.max_score:
            errors["max_score"] = "La nota maxima debe ser mayor o igual a la minima."
        if self.setting_id and (
            self.min_score < self.setting.score_min
            or self.max_score > self.setting.score_max
        ):
            errors["min_score"] = "El rango debe estar dentro de la escala configurada."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
