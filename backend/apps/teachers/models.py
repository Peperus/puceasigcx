from django.core.exceptions import ValidationError
from django.db import models

from apps.academic_catalogs.models import AcademicDomain
from apps.core.models import TimeStampedModel
from apps.people.models import Person


class TeacherStatus(models.TextChoices):
    ACTIVE = "activo", "Activo"
    INACTIVE = "inactivo", "Inactivo"
    GUEST = "invitado", "Invitado"
    CO_TEACHER = "codocente", "Codocente"
    EXTERNAL = "externo", "Externo"


class Teacher(TimeStampedModel):
    person = models.OneToOneField(
        Person,
        on_delete=models.PROTECT,
        related_name="teacher_profile",
        verbose_name="persona",
    )
    teacher_code = models.CharField("codigo docente", max_length=30, unique=True)
    academic_degree = models.CharField("grado academico", max_length=120, blank=True)
    professional_title = models.CharField(
        "titulo profesional",
        max_length=180,
        blank=True,
    )
    academic_profile = models.TextField("perfil academico/profesional", blank=True)
    institutional_phone = models.CharField(
        "telefono institucional",
        max_length=30,
        blank=True,
    )
    status = models.CharField(
        "estado",
        max_length=20,
        choices=TeacherStatus.choices,
        default=TeacherStatus.ACTIVE,
    )
    domains = models.ManyToManyField(
        AcademicDomain,
        related_name="teachers",
        blank=True,
        verbose_name="dominios o areas",
    )

    class Meta:
        ordering = ["person__last_name", "person__first_name", "teacher_code"]
        verbose_name = "docente"
        verbose_name_plural = "docentes"
        indexes = [
            models.Index(fields=["teacher_code"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.teacher_code} - {self.person.full_name}"


class OfficeHourModality(models.TextChoices):
    IN_PERSON = "presencial", "Presencial"
    VIRTUAL = "virtual", "Virtual"


class WeekDay(models.IntegerChoices):
    MONDAY = 1, "Lunes"
    TUESDAY = 2, "Martes"
    WEDNESDAY = 3, "Miercoles"
    THURSDAY = 4, "Jueves"
    FRIDAY = 5, "Viernes"
    SATURDAY = 6, "Sabado"
    SUNDAY = 7, "Domingo"


class TeacherOfficeHour(TimeStampedModel):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="office_hours",
        verbose_name="docente",
    )
    modality = models.CharField(
        "modalidad",
        max_length=20,
        choices=OfficeHourModality.choices,
    )
    day_of_week = models.PositiveSmallIntegerField(
        "dia",
        choices=WeekDay.choices,
    )
    start_time = models.TimeField("hora inicio")
    end_time = models.TimeField("hora fin")
    location_or_link = models.CharField("lugar o enlace", max_length=255)

    class Meta:
        ordering = ["teacher", "day_of_week", "start_time"]
        verbose_name = "horario de atencion docente"
        verbose_name_plural = "horarios de atencion docente"
        indexes = [
            models.Index(fields=["teacher", "day_of_week"]),
        ]

    def __str__(self):
        return (
            f"{self.teacher} - {self.get_day_of_week_display()} "
            f"{self.start_time}-{self.end_time}"
        )

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError(
                {"end_time": "La hora de fin debe ser posterior al inicio."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
