import pytest
from django.core.management import call_command

from apps.academic_catalogs.models import (
    AcademicPeriod,
    Career,
    CurriculumPrerequisite,
    GradingSystem,
    Subject,
)


@pytest.mark.django_db
def test_seed_academic_catalogs_is_idempotent():
    call_command("seed_academic_catalogs")
    call_command("seed_academic_catalogs")

    assert AcademicPeriod.objects.filter(code="2026-1").count() == 1
    assert Career.objects.filter(code="CAR-DEMO").count() == 1
    assert Subject.objects.filter(code="DEMO-101").count() == 1
    assert CurriculumPrerequisite.objects.count() == 1
    assert set(GradingSystem.objects.values_list("code", flat=True)) == {
        "S1",
        "S2",
        "S3",
    }
