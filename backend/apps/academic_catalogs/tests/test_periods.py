from datetime import date

import pytest
from django.core.exceptions import ValidationError

from apps.academic_catalogs.models import AcademicPeriod, PeriodStatus
from apps.academic_catalogs.tests.factories import make_period


@pytest.mark.django_db
def test_academic_period_can_be_created():
    period = make_period(code="2026-A", is_current=True)

    assert period.code == "2026-A"
    assert period.is_current is True


@pytest.mark.django_db
def test_only_one_current_period_is_allowed():
    make_period(code="2026-A", is_current=True)

    with pytest.raises(ValidationError):
        make_period(code="2026-B", is_current=True)


@pytest.mark.django_db
def test_active_periods_cannot_overlap():
    make_period(code="2026-A", status=PeriodStatus.ACTIVE)

    with pytest.raises(ValidationError):
        AcademicPeriod.objects.create(
            name="Periodo solapado",
            code="2026-B",
            start_date=date(2026, 6, 1),
            end_date=date(2026, 12, 15),
            enrollment_start_date=date(2026, 6, 1),
            enrollment_end_date=date(2026, 6, 30),
            status=PeriodStatus.ACTIVE,
        )


@pytest.mark.django_db
def test_enrollment_dates_must_be_inside_period():
    with pytest.raises(ValidationError):
        AcademicPeriod.objects.create(
            name="Periodo invalido",
            code="2026-C",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 6, 30),
            enrollment_start_date=date(2025, 12, 1),
            enrollment_end_date=date(2026, 1, 15),
        )
