from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AcademicDashboardView, AcademicGradeQueryView, GradeExportView

router = DefaultRouter()

urlpatterns = [
    path(
        "academic-dashboard/",
        AcademicDashboardView.as_view(),
        name="academic-dashboard",
    ),
    path("grades/", AcademicGradeQueryView.as_view(), name="academic-grade-query"),
    path("grades/export/", GradeExportView.as_view(), name="grade-export"),
    *router.urls,
]
