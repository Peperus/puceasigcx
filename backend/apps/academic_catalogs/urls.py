from rest_framework.routers import DefaultRouter

from .views import (
    AcademicDomainViewSet,
    AcademicLevelViewSet,
    AcademicPeriodViewSet,
    AcademicSettingViewSet,
    AchievementLevelViewSet,
    CareerViewSet,
    CurriculumPrerequisiteViewSet,
    CurriculumSubjectViewSet,
    FacultyOrUnitViewSet,
    GradingSystemViewSet,
    ModalityViewSet,
    StudyPlanViewSet,
    SubjectViewSet,
)

router = DefaultRouter()
router.register("periods", AcademicPeriodViewSet, basename="academic-period")
router.register("faculties", FacultyOrUnitViewSet, basename="faculty-or-unit")
router.register("modalities", ModalityViewSet, basename="modality")
router.register("domains", AcademicDomainViewSet, basename="academic-domain")
router.register("careers", CareerViewSet, basename="career")
router.register("study-plans", StudyPlanViewSet, basename="study-plan")
router.register("levels", AcademicLevelViewSet, basename="academic-level")
router.register("grading-systems", GradingSystemViewSet, basename="grading-system")
router.register("subjects", SubjectViewSet, basename="subject")
router.register(
    "curriculum-subjects",
    CurriculumSubjectViewSet,
    basename="curriculum-subject",
)
router.register(
    "curriculum-prerequisites",
    CurriculumPrerequisiteViewSet,
    basename="curriculum-prerequisite",
)
router.register("settings", AcademicSettingViewSet, basename="academic-setting")
router.register(
    "achievement-levels", AchievementLevelViewSet, basename="achievement-level"
)

urlpatterns = router.urls
