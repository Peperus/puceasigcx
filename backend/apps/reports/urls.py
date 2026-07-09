from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AcademicDashboardView

router = DefaultRouter()

urlpatterns = [
    path(
        "academic-dashboard/",
        AcademicDashboardView.as_view(),
        name="academic-dashboard",
    ),
    *router.urls,
]
