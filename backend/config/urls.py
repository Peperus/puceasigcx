from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.core.urls")),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/academic/", include("apps.academic_catalogs.urls")),
    path("api/people/", include("apps.people.urls")),
    path("api/students/", include("apps.students.urls")),
    path("api/teachers/", include("apps.teachers.urls")),
    path("api/enrollment/", include("apps.enrollment.urls")),
    path("api/syllabi/", include("apps.syllabus.urls")),
    path("api/grading/", include("apps.grading.urls")),
    path("api/documents/", include("apps.documents.urls")),
    path("api/reports/", include("apps.reports.urls")),
    path("api/audit/", include("apps.audit.urls")),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
