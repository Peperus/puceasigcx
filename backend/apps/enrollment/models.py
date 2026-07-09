from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone

from apps.academic_catalogs.models import (
    AcademicLevel,
    AcademicPeriod,
    Career,
    GradingSystem,
    Modality,
    StudyPlan,
    Subject,
)
from apps.core.models import TimeStampedModel
from apps.students.models import Student, StudentStatus
from apps.teachers.models import Teacher, TeacherStatus


class AcademicOfferStatus(models.TextChoices):
    DRAFT = "draft", "Borrador"
    PUBLISHED = "published", "Publicada"
    CLOSED = "closed", "Cerrada"
    ARCHIVED = "archived", "Archivada"


class AcademicOffer(TimeStampedModel):
    period = models.ForeignKey(
        AcademicPeriod,
        on_delete=models.PROTECT,
        related_name="academic_offers",
        verbose_name="periodo",
    )
    career = models.ForeignKey(
        Career,
        on_delete=models.PROTECT,
        related_name="academic_offers",
        verbose_name="carrera",
    )
    study_plan = models.ForeignKey(
        StudyPlan,
        on_delete=models.PROTECT,
        related_name="academic_offers",
        verbose_name="plan de estudio",
    )
    level = models.ForeignKey(
        AcademicLevel,
        on_delete=models.PROTECT,
        related_name="academic_offers",
        verbose_name="nivel",
    )
    status = models.CharField(
        "estado",
        max_length=20,
        choices=AcademicOfferStatus.choices,
        default=AcademicOfferStatus.DRAFT,
    )
    description = models.TextField("descripcion", blank=True)

    class Meta:
        ordering = ["period__code", "career__name", "level__order"]
        verbose_name = "oferta academica"
        verbose_name_plural = "ofertas academicas"
        constraints = [
            models.UniqueConstraint(
                fields=["period", "career", "study_plan", "level"],
                name="unique_academic_offer_period_career_plan_level",
            )
        ]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["period", "career"]),
        ]

    def __str__(self):
        return f"{self.period.code} - {self.career.code} - Nivel {self.level.number}"

    def clean(self):
        errors = {}
        if (
            self.study_plan_id
            and self.career_id
            and self.study_plan.career_id != self.career_id
        ):
            errors["study_plan"] = "El plan de estudio debe pertenecer a la carrera."
        if (
            self.level_id
            and self.study_plan_id
            and self.level.study_plan_id != self.study_plan_id
        ):
            errors["level"] = "El nivel debe pertenecer al plan de estudio."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class CourseSectionStatus(models.TextChoices):
    PLANNED = "planned", "Planificado"
    ACTIVE = "active", "Activo"
    CLOSED = "closed", "Cerrado"
    CANCELED = "canceled", "Cancelado"


class CourseSection(TimeStampedModel):
    offer = models.ForeignKey(
        AcademicOffer,
        on_delete=models.PROTECT,
        related_name="course_sections",
        verbose_name="oferta academica",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="course_sections",
        verbose_name="asignatura",
    )
    parallel = models.CharField("paralelo", max_length=20)
    capacity = models.PositiveSmallIntegerField(
        "cupo", validators=[MinValueValidator(1)]
    )
    modality = models.ForeignKey(
        Modality,
        on_delete=models.PROTECT,
        related_name="course_sections",
        verbose_name="modalidad",
    )
    grading_system = models.ForeignKey(
        GradingSystem,
        on_delete=models.PROTECT,
        related_name="course_sections",
        verbose_name="sistema de calificacion",
    )
    classroom = models.CharField("aula", max_length=80, blank=True)
    status = models.CharField(
        "estado",
        max_length=20,
        choices=CourseSectionStatus.choices,
        default=CourseSectionStatus.PLANNED,
    )

    class Meta:
        ordering = ["offer", "subject__code", "parallel"]
        verbose_name = "curso/paralelo"
        verbose_name_plural = "cursos/paralelos"
        constraints = [
            models.UniqueConstraint(
                fields=["offer", "subject", "parallel"],
                name="unique_course_section_offer_subject_parallel",
            )
        ]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["parallel"]),
        ]

    def __str__(self):
        return f"{self.subject.code} {self.parallel} - {self.offer.period.code}"

    def clean(self):
        errors = {}
        if (
            self.subject_id
            and self.offer_id
            and self.subject.career_id != self.offer.career_id
        ):
            errors["subject"] = "La asignatura debe pertenecer a la carrera ofertada."
        if self.grading_system_id and not self.grading_system.is_active:
            errors["grading_system"] = "El sistema de calificacion debe estar activo."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def enrolled_count(self):
        return self.course_enrollments.filter(
            status=CourseEnrollmentStatus.ENROLLED
        ).count()

    @property
    def available_seats(self):
        return max(self.capacity - self.enrolled_count, 0)


class TeachingRole(models.TextChoices):
    LEAD = "lead", "Titular"
    CO_TEACHER = "co_teacher", "Codocente"


class TeachingAssignmentStatus(models.TextChoices):
    ACTIVE = "active", "Activo"
    INACTIVE = "inactive", "Inactivo"


class TeachingAssignment(TimeStampedModel):
    course_section = models.ForeignKey(
        CourseSection,
        on_delete=models.CASCADE,
        related_name="teaching_assignments",
        verbose_name="curso/paralelo",
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        related_name="teaching_assignments",
        verbose_name="docente",
    )
    role = models.CharField(
        "rol docente",
        max_length=20,
        choices=TeachingRole.choices,
        default=TeachingRole.LEAD,
    )
    weekly_hours = models.DecimalField(
        "carga horaria semanal",
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    status = models.CharField(
        "estado",
        max_length=20,
        choices=TeachingAssignmentStatus.choices,
        default=TeachingAssignmentStatus.ACTIVE,
    )

    class Meta:
        ordering = ["course_section", "role", "teacher__person__last_name"]
        verbose_name = "asignacion docente"
        verbose_name_plural = "asignaciones docentes"
        constraints = [
            models.UniqueConstraint(
                fields=["course_section", "teacher", "role"],
                name="unique_teacher_assignment_role_per_course",
            ),
            models.UniqueConstraint(
                fields=["course_section", "role"],
                condition=Q(
                    role=TeachingRole.LEAD,
                    status=TeachingAssignmentStatus.ACTIVE,
                ),
                name="unique_active_lead_teacher_per_course",
            ),
        ]

    def __str__(self):
        return f"{self.teacher} - {self.course_section} ({self.get_role_display()})"

    def clean(self):
        errors = {}
        if self.teacher_id and self.teacher.status != TeacherStatus.ACTIVE:
            errors["teacher"] = "El docente debe estar activo."
        if self.weekly_hours is not None and self.weekly_hours < 0:
            errors["weekly_hours"] = "La carga horaria no puede ser negativa."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class EnrollmentStatus(models.TextChoices):
    ENROLLED = "enrolled", "Matriculado"
    WITHDRAWN = "withdrawn", "Retirado"
    APPROVED = "approved", "Aprobado"
    FAILED = "failed", "Reprobado"
    HOMOLOGATED = "homologated", "Homologado"
    ANNULLED = "annulled", "Anulado"


class Enrollment(TimeStampedModel):
    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="enrollments",
        verbose_name="estudiante",
    )
    period = models.ForeignKey(
        AcademicPeriod,
        on_delete=models.PROTECT,
        related_name="enrollments",
        verbose_name="periodo",
    )
    career = models.ForeignKey(
        Career,
        on_delete=models.PROTECT,
        related_name="enrollments",
        verbose_name="carrera",
    )
    study_plan = models.ForeignKey(
        StudyPlan,
        on_delete=models.PROTECT,
        related_name="enrollments",
        null=True,
        blank=True,
        verbose_name="plan de estudio",
    )
    status = models.CharField(
        "estado",
        max_length=20,
        choices=EnrollmentStatus.choices,
        default=EnrollmentStatus.ENROLLED,
    )
    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        related_name="created_enrollments",
        null=True,
        blank=True,
        verbose_name="creado por",
    )

    class Meta:
        ordering = ["-period__start_date", "student__student_code"]
        verbose_name = "matricula academica"
        verbose_name_plural = "matriculas academicas"
        constraints = [
            models.UniqueConstraint(
                fields=["student", "period"],
                name="unique_enrollment_student_period",
            )
        ]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["period", "career"]),
        ]

    def __str__(self):
        return f"{self.student.student_code} - {self.period.code}"

    def clean(self):
        errors = {}
        if self.student_id and self.student.status != StudentStatus.ACTIVE:
            errors["student"] = "El estudiante debe estar activo."
        if (
            self.student_id
            and self.career_id
            and self.student.career_id != self.career_id
        ):
            errors["career"] = "La matricula debe usar la carrera del estudiante."
        if (
            self.study_plan_id
            and self.career_id
            and self.study_plan.career_id != self.career_id
        ):
            errors["study_plan"] = "El plan de estudio debe pertenecer a la carrera."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.student_id:
            self.career_id = self.career_id or self.student.career_id
            self.study_plan_id = self.study_plan_id or self.student.study_plan_id
        self.full_clean()
        super().save(*args, **kwargs)


class CourseEnrollmentStatus(models.TextChoices):
    ENROLLED = "enrolled", "Matriculado"
    WITHDRAWN = "withdrawn", "Retirado"
    APPROVED = "approved", "Aprobado"
    FAILED = "failed", "Reprobado"
    HOMOLOGATED = "homologated", "Homologado"
    ANNULLED = "annulled", "Anulado"


class CourseEnrollment(TimeStampedModel):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="course_enrollments",
        verbose_name="matricula",
    )
    course_section = models.ForeignKey(
        CourseSection,
        on_delete=models.PROTECT,
        related_name="course_enrollments",
        verbose_name="curso/paralelo",
    )
    status = models.CharField(
        "estado",
        max_length=20,
        choices=CourseEnrollmentStatus.choices,
        default=CourseEnrollmentStatus.ENROLLED,
    )
    enrolled_at = models.DateTimeField("fecha de inscripcion", default=timezone.now)
    withdrawn_at = models.DateTimeField("fecha de retiro", null=True, blank=True)

    class Meta:
        ordering = ["enrollment", "course_section__subject__code"]
        verbose_name = "matricula en curso"
        verbose_name_plural = "matriculas en curso"
        constraints = [
            models.UniqueConstraint(
                fields=["enrollment", "course_section"],
                name="unique_course_enrollment_per_enrollment_course",
            )
        ]
        indexes = [
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.enrollment.student.student_code} - {self.course_section}"

    def clean(self):
        errors = {}
        if self.enrollment_id and self.course_section_id:
            offer = self.course_section.offer
            if self.enrollment.period_id != offer.period_id:
                errors["course_section"] = "El curso debe pertenecer al mismo periodo."
            if self.enrollment.career_id != offer.career_id:
                errors["course_section"] = (
                    "El curso debe pertenecer a la misma carrera."
                )
            if (
                self.enrollment.study_plan_id
                and self.enrollment.study_plan_id != offer.study_plan_id
            ):
                errors["course_section"] = (
                    "El curso debe pertenecer al mismo plan de estudio."
                )
            if self.status == CourseEnrollmentStatus.ENROLLED:
                if self.course_section.status != CourseSectionStatus.ACTIVE:
                    errors["course_section"] = (
                        "Solo se puede matricular en cursos activos."
                    )
                enrolled_count = CourseEnrollment.objects.filter(
                    course_section=self.course_section,
                    status=CourseEnrollmentStatus.ENROLLED,
                )
                if self.pk:
                    enrolled_count = enrolled_count.exclude(pk=self.pk)
                if enrolled_count.count() >= self.course_section.capacity:
                    errors["course_section"] = "El curso no tiene cupos disponibles."
        if (
            self.status == CourseEnrollmentStatus.WITHDRAWN
            and self.withdrawn_at is None
        ):
            self.withdrawn_at = timezone.now()
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class HomologationStatus(models.TextChoices):
    DRAFT = "draft", "Borrador"
    REGISTERED = "registered", "Registrada"
    APPROVED = "approved", "Aprobada"
    REJECTED = "rejected", "Rechazada"
    ANNULLED = "annulled", "Anulada"


class Homologation(TimeStampedModel):
    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="homologations",
        verbose_name="estudiante",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="homologations",
        verbose_name="asignatura",
    )
    period = models.ForeignKey(
        AcademicPeriod,
        on_delete=models.PROTECT,
        related_name="homologations",
        verbose_name="periodo",
    )
    resolution_reference = models.CharField(
        "resolucion o referencia",
        max_length=120,
    )
    observations = models.TextField("observaciones", blank=True)
    status = models.CharField(
        "estado",
        max_length=20,
        choices=HomologationStatus.choices,
        default=HomologationStatus.REGISTERED,
    )
    registered_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        related_name="registered_homologations",
        null=True,
        blank=True,
        verbose_name="registrado por",
    )

    class Meta:
        ordering = ["-created_at", "student__student_code", "subject__code"]
        verbose_name = "homologacion"
        verbose_name_plural = "homologaciones"
        constraints = [
            models.UniqueConstraint(
                fields=["student", "subject", "period"],
                name="unique_homologation_student_subject_period",
            )
        ]

    def __str__(self):
        return f"{self.student.student_code} - {self.subject.code} ({self.period.code})"

    def clean(self):
        if (
            self.student_id
            and self.subject_id
            and self.student.career_id != self.subject.career_id
        ):
            raise ValidationError(
                {
                    "subject": (
                        "La asignatura debe pertenecer a la carrera del estudiante."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
