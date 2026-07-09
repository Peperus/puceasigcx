"""Transactional services for people domain."""

import csv
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from django.contrib.auth import get_user_model
from django.db import transaction

from apps.academic_catalogs.models import (
    AcademicDomain,
    AcademicPeriod,
    Career,
    StudyPlan,
)
from apps.audit.services import log_event
from apps.students.models import Student
from apps.teachers.models import Teacher

from .models import IdentificationType, Person

REQUIRED_COLUMNS = {
    "record_type",
    "first_name",
    "last_name",
}


@dataclass
class ImportRowError:
    row_number: int
    message: str


@dataclass
class ImportPeopleResult:
    created: int = 0
    updated: int = 0
    rejected: int = 0
    errors: list[ImportRowError] = field(default_factory=list)

    def as_dict(self):
        return {
            "created": self.created,
            "updated": self.updated,
            "rejected": self.rejected,
            "errors": [
                {"row_number": error.row_number, "message": error.message}
                for error in self.errors
            ],
        }


def import_people_csv(
    path,
    *,
    user=None,
    update_existing=True,
    tolerate_errors=True,
    request=None,
):
    csv_path = Path(path)
    result = ImportPeopleResult()

    with csv_path.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing_columns:
            raise ValueError(
                "Columnas obligatorias faltantes: " + ", ".join(sorted(missing_columns))
            )

        for row_number, row in enumerate(reader, start=2):
            try:
                created_count, updated_count = _import_people_row(
                    _normalize_row(row),
                    update_existing=update_existing,
                )
            except Exception as exc:
                result.rejected += 1
                result.errors.append(ImportRowError(row_number, str(exc)))
                if not tolerate_errors:
                    raise
            else:
                result.created += created_count
                result.updated += updated_count

    log_event(
        action="people_imported",
        module="people",
        user=user,
        model_name="Person",
        new_data=result.as_dict(),
        reason=f"Importacion CSV: {csv_path.name}",
        request=request,
    )
    return result


@transaction.atomic
def _import_people_row(row, *, update_existing):
    record_types = {
        part.strip().lower()
        for part in row["record_type"].replace(";", ",").split(",")
        if part.strip()
    }
    if not record_types:
        raise ValueError("record_type es obligatorio.")

    person, person_created = _upsert_person(row, update_existing=update_existing)
    created_count = int(person_created)
    updated_count = int(not person_created)

    if "student" in record_types or "estudiante" in record_types:
        created = _upsert_student(person, row, update_existing=update_existing)
        created_count += int(created)
        updated_count += int(not created)

    if "teacher" in record_types or "docente" in record_types:
        created = _upsert_teacher(person, row, update_existing=update_existing)
        created_count += int(created)
        updated_count += int(not created)

    return created_count, updated_count


def _upsert_person(row, *, update_existing):
    lookup = _person_lookup(row)
    if not lookup:
        raise ValueError("Debe existir identificacion, correo o user_email.")

    defaults = {
        "identification_type": row.get("identification_type")
        or IdentificationType.CEDULA,
        "identification_number": row.get("identification_number") or None,
        "first_name": row["first_name"],
        "last_name": row["last_name"],
        "institutional_email": row.get("institutional_email", ""),
        "personal_email": row.get("personal_email", ""),
        "phone": row.get("phone", ""),
        "birth_date": _parse_date(row.get("birth_date")),
        "address": row.get("address", ""),
        "is_active": _parse_bool(row.get("is_active"), default=True),
    }
    user = _user_from_email(row.get("user_email"))
    if user is not None:
        defaults["user"] = user

    person = Person.objects.filter(**lookup).first()
    if person:
        if not update_existing:
            raise ValueError("La persona ya existe y update_existing esta desactivado.")
        for field_name, value in defaults.items():
            setattr(person, field_name, value)
        person.save()
        return person, False

    person = Person.objects.create(**defaults)
    return person, True


def _upsert_student(person, row, *, update_existing):
    student_code = row.get("student_code")
    career_code = row.get("career_code")
    if not student_code or not career_code:
        raise ValueError("student_code y career_code son obligatorios para estudiante.")

    career = Career.objects.get(code=career_code)
    defaults = {
        "person": person,
        "career": career,
        "study_plan": _study_plan(row.get("study_plan_code"), career),
        "admission_period": _academic_period(row.get("admission_period_code")),
        "admission_date": _parse_date(row.get("admission_date")),
        "status": row.get("student_status") or row.get("status") or "activo",
        "observations": row.get("observations", ""),
    }
    student = Student.objects.filter(student_code=student_code).first()
    if student:
        if not update_existing:
            raise ValueError(
                "El estudiante ya existe y update_existing esta desactivado."
            )
        for field_name, value in defaults.items():
            setattr(student, field_name, value)
        student.save()
        return False

    Student.objects.create(student_code=student_code, **defaults)
    return True


def _upsert_teacher(person, row, *, update_existing):
    teacher_code = row.get("teacher_code")
    if not teacher_code:
        raise ValueError("teacher_code es obligatorio para docente.")

    defaults = {
        "person": person,
        "academic_degree": row.get("academic_degree", ""),
        "professional_title": row.get("professional_title", ""),
        "academic_profile": row.get("academic_profile", ""),
        "institutional_phone": row.get("institutional_phone", ""),
        "status": row.get("teacher_status") or row.get("status") or "activo",
    }
    teacher = Teacher.objects.filter(teacher_code=teacher_code).first()
    if teacher:
        if not update_existing:
            raise ValueError("El docente ya existe y update_existing esta desactivado.")
        for field_name, value in defaults.items():
            setattr(teacher, field_name, value)
        teacher.save()
        created = False
    else:
        teacher = Teacher.objects.create(teacher_code=teacher_code, **defaults)
        created = True

    domain_codes = _split_codes(row.get("domain_codes", ""))
    if domain_codes:
        teacher.domains.set(AcademicDomain.objects.filter(code__in=domain_codes))

    return created


def _normalize_row(row):
    normalized = {}
    for key, value in row.items():
        if key is None:
            continue
        normalized[key] = (value or "").strip()
    return normalized


def _person_lookup(row):
    if row.get("identification_number"):
        return {"identification_number": row["identification_number"]}
    if row.get("institutional_email"):
        return {"institutional_email__iexact": row["institutional_email"]}
    user = _user_from_email(row.get("user_email"))
    return {"user": user} if user else {}


def _user_from_email(email):
    if not email:
        return None
    return get_user_model().objects.filter(email__iexact=email).first()


def _study_plan(code, career):
    if not code:
        return None
    return StudyPlan.objects.get(code=code, career=career)


def _academic_period(code):
    if not code:
        return None
    return AcademicPeriod.objects.get(code=code)


def _parse_date(value):
    if not value:
        return None
    return date.fromisoformat(value)


def _parse_bool(value, *, default):
    if not value:
        return default
    return value.lower() in {"1", "true", "si", "yes", "activo"}


def _split_codes(value):
    return [part.strip() for part in value.replace(";", ",").split(",") if part.strip()]
