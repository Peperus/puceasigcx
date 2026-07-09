from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q

from apps.core.models import TimeStampedModel


class IdentificationType(models.TextChoices):
    CEDULA = "cedula", "Cedula"
    PASSPORT = "passport", "Pasaporte"
    RUC = "ruc", "RUC"
    OTHER = "other", "Otro"


class Person(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="person",
        null=True,
        blank=True,
        verbose_name="usuario",
    )
    identification_type = models.CharField(
        "tipo de identificacion",
        max_length=20,
        choices=IdentificationType.choices,
        default=IdentificationType.CEDULA,
    )
    identification_number = models.CharField(
        "numero de identificacion",
        max_length=30,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z0-9\-\.]+$",
                message=(
                    "La identificacion solo puede contener letras, numeros, "
                    "punto o guion."
                ),
            )
        ],
    )
    first_name = models.CharField("nombres", max_length=150)
    last_name = models.CharField("apellidos", max_length=150)
    institutional_email = models.EmailField(
        "correo institucional",
        blank=True,
    )
    personal_email = models.EmailField("correo personal", blank=True)
    phone = models.CharField("telefono", max_length=30, blank=True)
    birth_date = models.DateField("fecha de nacimiento", null=True, blank=True)
    address = models.TextField("direccion", blank=True)
    is_active = models.BooleanField("activo", default=True)

    class Meta:
        ordering = ["last_name", "first_name", "identification_number"]
        verbose_name = "persona"
        verbose_name_plural = "personas"
        constraints = [
            models.UniqueConstraint(
                fields=["identification_number"],
                condition=Q(identification_number__isnull=False)
                & ~Q(identification_number=""),
                name="unique_person_identification_when_present",
            )
        ]
        indexes = [
            models.Index(fields=["identification_number"]),
            models.Index(fields=["last_name", "first_name"]),
            models.Index(fields=["institutional_email"]),
        ]

    def __str__(self):
        identifier = self.identification_number or "sin identificacion"
        return f"{self.full_name} ({identifier})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def save(self, *args, **kwargs):
        if self.identification_number == "":
            self.identification_number = None
        self.full_clean()
        super().save(*args, **kwargs)
