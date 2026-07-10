from rest_framework.routers import DefaultRouter

from .views import GradebookClosureViewSet, TeacherGradebookViewSet

router = DefaultRouter()
router.register(
    "teacher/gradebooks",
    TeacherGradebookViewSet,
    basename="teacher-gradebook",
)
router.register("gradebooks", GradebookClosureViewSet, basename="gradebook")

urlpatterns = router.urls
