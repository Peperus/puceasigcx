from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

from apps.core.models import TimeStampedModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("El correo institucional es obligatorio.")

        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    email = models.EmailField("correo institucional", unique=True)
    names = models.CharField("nombres", max_length=150)
    last_names = models.CharField("apellidos", max_length=150)
    identification = models.CharField(
        "identificacion",
        max_length=30,
        unique=True,
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
    phone = models.CharField("telefono", max_length=30, blank=True)
    is_active = models.BooleanField("activo", default=True)
    is_staff = models.BooleanField("acceso admin", default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["names", "last_names", "identification"]

    class Meta:
        ordering = ["last_names", "names", "email"]
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.names} {self.last_names}".strip()


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    primary_role = models.CharField("rol principal", max_length=80, blank=True)
    institutional_person_reference = models.CharField(
        "referencia persona institucional",
        max_length=80,
        blank=True,
        help_text="Referencia temporal hasta implementar el modelo Person.",
    )
    must_change_password = models.BooleanField(default=False)
    security_questions_configured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "perfil de usuario"
        verbose_name_plural = "perfiles de usuario"

    def __str__(self):
        return f"Perfil de {self.user.email}"
