"""Transactional services for academic catalogs domain."""

from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from .models import AcademicSetting, AchievementLevel, GradingSystem

DEFAULT_GRADING_SYSTEMS = (
    (
        "S1",
        "Sistema S1 por resultados de aprendizaje",
        {
            "learning_outcomes": 3,
            "recovery_policy": "strict_per_learning_outcome",
        },
    ),
    (
        "S2",
        "Sistema S2 con recuperacion de un resultado",
        {
            "learning_outcomes": 3,
            "recovery_policy": "single_failed_learning_outcome",
        },
    ),
    (
        "S3",
        "Sistema S3 por parciales",
        {
            "partials": 3,
            "recovery_policy": "final_evaluation_when_average_below_threshold",
        },
    ),
)

DEFAULT_ACHIEVEMENT_LEVELS = (
    ("A", Decimal("45.00"), Decimal("50.00"), "Alcanzado con excelencia"),
    ("B", Decimal("40.00"), Decimal("44.99"), "Alcanzado muy bien"),
    ("C", Decimal("30.00"), Decimal("39.99"), "Alcanzado"),
    ("D", Decimal("0.00"), Decimal("29.99"), "No alcanzado"),
)


@transaction.atomic
def ensure_default_grading_systems():
    systems = {}
    for code, name, config in DEFAULT_GRADING_SYSTEMS:
        system, _ = GradingSystem.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "description": name,
                "config": config,
                "is_active": True,
            },
        )
        systems[code] = system
    return systems


@transaction.atomic
def ensure_default_academic_setting():
    systems = ensure_default_grading_systems()
    setting, _ = AcademicSetting.objects.update_or_create(
        is_default=True,
        defaults={
            "name": "Configuracion academica general",
            "score_min": Decimal("0.00"),
            "score_max": Decimal("50.00"),
            "passing_score": Decimal("30.00"),
            "default_grading_system": systems["S1"],
        },
    )

    for letter, min_score, max_score, description in DEFAULT_ACHIEVEMENT_LEVELS:
        AchievementLevel.objects.update_or_create(
            setting=setting,
            letter=letter,
            defaults={
                "min_score": min_score,
                "max_score": max_score,
                "description": description,
            },
        )

    return setting


def get_effective_academic_setting(period=None, career=None):
    queryset = AcademicSetting.objects.select_related(
        "period",
        "career",
        "default_grading_system",
    ).prefetch_related("achievement_levels")

    if period and career:
        try:
            return queryset.get(period=period, career=career)
        except AcademicSetting.DoesNotExist:
            pass

    if career:
        try:
            return queryset.get(period__isnull=True, career=career)
        except AcademicSetting.DoesNotExist:
            pass

    if period:
        try:
            return queryset.get(period=period, career__isnull=True)
        except AcademicSetting.DoesNotExist:
            pass

    try:
        return queryset.get(is_default=True)
    except AcademicSetting.DoesNotExist as exc:
        raise ObjectDoesNotExist(
            "No existe una configuracion academica por defecto."
        ) from exc
