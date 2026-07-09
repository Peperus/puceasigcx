from rest_framework.routers import DefaultRouter

from .views import TeacherOfficeHourViewSet, TeacherViewSet

router = DefaultRouter()
router.register(
    "office-hours", TeacherOfficeHourViewSet, basename="teacher-office-hour"
)
router.register("", TeacherViewSet, basename="teacher")

urlpatterns = router.urls
