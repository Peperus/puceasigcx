import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import override_settings
from django.urls import path
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework.views import APIView

from apps.core.permissions import IsAcademicStaff, IsTeacher


class TeacherOnlyProbeView(APIView):
    permission_classes = [IsTeacher]

    def get(self, request):
        return Response({"ok": True})


class AcademicStaffProbeView(APIView):
    permission_classes = [IsAcademicStaff]

    def get(self, request):
        return Response({"ok": True})


urlpatterns = [
    path("teacher-only/", TeacherOnlyProbeView.as_view()),
    path("academic-staff/", AcademicStaffProbeView.as_view()),
]


def make_user(email, identification, group_name=None):
    user = get_user_model().objects.create_user(
        email=email,
        password="Str0ng-pass-demo",
        names="Usuario",
        last_names="Sintetico",
        identification=identification,
    )
    if group_name:
        user.groups.add(Group.objects.create(name=group_name))
    return user


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=__name__)
def test_user_without_required_role_receives_403():
    user = make_user("estudiante-perm@example.edu", "ID-PERM-001", "Estudiante")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/teacher-only/")

    assert response.status_code == 403


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=__name__)
def test_user_with_required_role_can_access():
    user = make_user("docente-perm@example.edu", "ID-PERM-002", "Docente")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/teacher-only/")

    assert response.status_code == 200


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=__name__)
def test_academic_staff_allows_institutional_staff_roles():
    user = make_user(
        "secretaria-perm@example.edu",
        "ID-PERM-003",
        "Secretaria",
    )
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/academic-staff/")

    assert response.status_code == 200
