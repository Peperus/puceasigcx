from rest_framework.routers import DefaultRouter

from .views import (
    SyllabusAchievementLevelViewSet,
    SyllabusBibliographyViewSet,
    SyllabusCompetencyViewSet,
    SyllabusCriterionViewSet,
    SyllabusLearningOutcomeViewSet,
    SyllabusViewSet,
    SyllabusWeeklyPlanViewSet,
)

router = DefaultRouter()
router.register(
    "competencies", SyllabusCompetencyViewSet, basename="syllabus-competency"
)
router.register(
    "learning-outcomes",
    SyllabusLearningOutcomeViewSet,
    basename="syllabus-learning-outcome",
)
router.register("criteria", SyllabusCriterionViewSet, basename="syllabus-criterion")
router.register(
    "achievement-levels",
    SyllabusAchievementLevelViewSet,
    basename="syllabus-achievement-level",
)
router.register(
    "bibliography", SyllabusBibliographyViewSet, basename="syllabus-bibliography"
)
router.register(
    "weekly-plans", SyllabusWeeklyPlanViewSet, basename="syllabus-weekly-plan"
)
router.register("", SyllabusViewSet, basename="syllabus")

urlpatterns = router.urls
