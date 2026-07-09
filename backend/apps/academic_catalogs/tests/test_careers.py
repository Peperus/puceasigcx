import pytest
from django.db import IntegrityError

from apps.academic_catalogs.models import AcademicDomain, Career, Modality
from apps.academic_catalogs.tests.factories import (
    make_career,
    make_domain,
    make_modality,
)


@pytest.mark.django_db
def test_career_modality_and_domain_can_be_created():
    career = make_career(code="ADM")

    assert career.modality.name == "Modalidad MOD-ADM"
    assert career.domain.name == "Dominio DOM-ADM"


@pytest.mark.django_db
def test_catalog_codes_are_unique():
    make_modality(code="DIST")

    with pytest.raises(IntegrityError):
        Modality.objects.create(code="DIST", name="Duplicada")


@pytest.mark.django_db
def test_career_codes_are_unique():
    career = make_career(code="GST")

    with pytest.raises(IntegrityError):
        Career.objects.create(
            code="GST",
            name="Carrera duplicada",
            modality=career.modality,
        )


@pytest.mark.django_db
def test_domain_codes_are_unique():
    make_domain(code="SALUD")

    with pytest.raises(IntegrityError):
        AcademicDomain.objects.create(code="SALUD", name="Dominio duplicado")
