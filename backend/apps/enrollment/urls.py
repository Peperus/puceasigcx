from rest_framework.routers import DefaultRouter

from .views import (
    AcademicOfferViewSet,
    CourseEnrollmentViewSet,
    CourseSectionViewSet,
    EnrollmentRecordViewSet,
    HomologationViewSet,
    TeachingAssignmentViewSet,
)

router = DefaultRouter()
router.register("academic-offers", AcademicOfferViewSet, basename="academic-offer")
router.register("course-sections", CourseSectionViewSet, basename="course-section")
router.register(
    "teaching-assignments",
    TeachingAssignmentViewSet,
    basename="teaching-assignment",
)
router.register("enrollments", EnrollmentRecordViewSet, basename="enrollment")
router.register(
    "course-enrollments",
    CourseEnrollmentViewSet,
    basename="course-enrollment",
)
router.register("homologations", HomologationViewSet, basename="homologation")

urlpatterns = router.urls
