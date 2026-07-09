from decimal import Decimal

import pytest
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from apps.academic_catalogs.models import AcademicSetting
from apps.academic_catalogs.services import (
    ensure_default_academic_setting,
    get_effective_academic_setting,
)
from apps.academic_catalogs.tests.factories import make_career, make_period


@pytest.mark.django_db
def test_default_academic_setting_contains_base_scale_and_letters():
    setting = ensure_default_academic_setting()

    assert setting.score_min == Decimal("0.00")
    assert setting.score_max == Decimal("50.00")
    assert setting.passing_score == Decimal("30.00")
    assert set(setting.achievement_levels.values_list("letter", flat=True)) == {
        "A",
        "B",
        "C",
        "D",
    }


@pytest.mark.django_db
def test_effective_setting_prefers_period_and_career_specific_configuration():
    default_setting = ensure_default_academic_setting()
    period = make_period(code="2026-CFG")
    career = make_career(code="CFG")
    specific_setting = AcademicSetting.objects.create(
        name="Configuracion especifica",
        period=period,
        career=career,
        score_min=0,
        score_max=50,
        passing_score=32,
        default_grading_system=default_setting.default_grading_system,
    )

    assert (
        get_effective_academic_setting(period=period, career=career) == specific_setting
    )


@pytest.mark.django_db
def test_setting_threshold_must_be_inside_scale():
    with pytest.raises(ValidationError):
        AcademicSetting.objects.create(
            name="Configuracion invalida",
            score_min=0,
            score_max=50,
            passing_score=60,
        )


@pytest.mark.django_db
def test_missing_default_setting_raises_explicit_error():
    with pytest.raises(ObjectDoesNotExist):
        get_effective_academic_setting()
