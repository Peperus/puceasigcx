from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AcademicDashboardView,
    AcademicGradeQueryView,
    GradeExportView,
    MvpReportView,
)

router = DefaultRouter()

urlpatterns = [
    path(
        "academic-dashboard/",
        AcademicDashboardView.as_view(),
        name="academic-dashboard",
    ),
    path("grades/", AcademicGradeQueryView.as_view(), name="academic-grade-query"),
    path("grades/export/", GradeExportView.as_view(), name="grade-export"),
    path("mvp/<slug:report_type>/", MvpReportView.as_view(), name="mvp-report"),
    *router.urls,
]
