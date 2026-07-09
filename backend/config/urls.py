from django.contrib import admin
from django.urls import include, path

from apps.accounts.views import CurrentUserView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.core.urls")),
    path("api/", include("apps.accounts.urls")),
    path("api/me/", CurrentUserView.as_view(), name="me"),
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
]
