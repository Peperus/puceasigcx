import pytest
from django.core.exceptions import ValidationError

from apps.academic_catalogs.tests.factories import make_career, make_level, make_plan
from apps.enrollment.models import AcademicOffer, AcademicOfferStatus
from apps.enrollment.tests.factories import make_offer


@pytest.mark.django_db
def test_can_create_academic_offer_by_period_career_plan_and_level():
    offer = make_offer("S4T1")

    assert offer.status == AcademicOfferStatus.DRAFT
    assert offer.period is not None
    assert offer.career == offer.study_plan.career
    assert offer.level.study_plan == offer.study_plan


@pytest.mark.django_db
def test_academic_offer_rejects_duplicate_period_career_plan_level():
    offer = make_offer("S4T1DUP")

    with pytest.raises(ValidationError):
        AcademicOffer.objects.create(
            period=offer.period,
            career=offer.career,
            study_plan=offer.study_plan,
            level=offer.level,
        )


@pytest.mark.django_db
def test_academic_offer_requires_level_from_same_plan():
    offer = make_offer("S4T1PLAN")
    other_plan = make_plan(
        career=make_career(code="CAR-S4T1-OTHER"),
        code="PLAN-S4T1-OTHER",
    )
    other_level = make_level(study_plan=other_plan, number=1)

    with pytest.raises(ValidationError):
        AcademicOffer.objects.create(
            period=offer.period,
            career=offer.career,
            study_plan=offer.study_plan,
            level=other_level,
        )
