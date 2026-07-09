from django.core.exceptions import ValidationError
from django.db import models

from apps.academic_catalogs.models import AcademicPeriod, Career, StudyPlan
from apps.core.models import TimeStampedModel
from apps.people.models import Person


class StudentStatus(models.TextChoices):
    CONVERTED_APPLICANT = "aspirante_convertido", "Aspirante convertido"
    ACTIVE = "activo", "Activo"
    WITHDRAWN = "retirado", "Retirado"
    GRADUATED_PENDING = "egresado", "Egresado"
    GRADUATED = "graduado", "Graduado"
    SUSPENDED = "suspendido", "Suspendido"
    ARCHIVED = "archivado", "Archivado"


class Student(TimeStampedModel):
    person = models.OneToOneField(
        Person,
        on_delete=models.PROTECT,
        related_name="student_profile",
        verbose_name="persona",
    )
    student_code = models.CharField("codigo estudiante", max_length=30, unique=True)
    career = models.ForeignKey(
        Career,
        on_delete=models.PROTECT,
        related_name="students",
        verbose_name="carrera principal",
    )
    study_plan = models.ForeignKey(
        StudyPlan,
        on_delete=models.PROTECT,
        related_name="students",
        null=True,
        blank=True,
        verbose_name="plan de estudio",
    )
    admission_period = models.ForeignKey(
        AcademicPeriod,
        on_delete=models.PROTECT,
        related_name="admitted_students",
        null=True,
        blank=True,
        verbose_name="periodo de ingreso",
    )
    admission_date = models.DateField("fecha de ingreso", null=True, blank=True)
    status = models.CharField(
        "estado",
        max_length=30,
        choices=StudentStatus.choices,
        default=StudentStatus.ACTIVE,
    )
    observations = models.TextField("observaciones", blank=True)

    class Meta:
        ordering = ["person__last_name", "person__first_name", "student_code"]
        verbose_name = "estudiante"
        verbose_name_plural = "estudiantes"
        indexes = [
            models.Index(fields=["student_code"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.student_code} - {self.person.full_name}"

    def clean(self):
        if (
            self.study_plan_id
            and self.career_id
            and self.study_plan.career_id != self.career_id
        ):
            raise ValidationError(
                {"study_plan": "El plan de estudio debe pertenecer a la carrera."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
