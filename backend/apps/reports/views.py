from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.academic_catalogs.models import AcademicPeriod
from apps.academic_catalogs.selectors import coordinator_career_ids
from apps.accounts.roles import (
    ROLE_ADMINISTRATOR,
    ROLE_CAREER_COORDINATOR,
    ROLE_SECRETARY,
    user_has_role,
)
from apps.enrollment.models import (
    CourseEnrollment,
    CourseEnrollmentStatus,
    CourseSection,
    Enrollment,
    TeachingAssignment,
    TeachingAssignmentStatus,
)


class CanViewAcademicDashboard(BasePermission):
    def has_permission(self, request, view):
        return bool(
            getattr(request.user, "is_authenticated", False)
            and user_has_role(
                request.user,
                ROLE_ADMINISTRATOR,
                ROLE_SECRETARY,
                ROLE_CAREER_COORDINATOR,
            )
        )


class AcademicDashboardView(APIView):
    permission_classes = [CanViewAcademicDashboard]

    def get(self, request):
        period = self._get_period(request)
        course_sections = CourseSection.objects.filter(offer__period=period)
        enrollments = Enrollment.objects.filter(period=period)

        if user_has_role(request.user, ROLE_CAREER_COORDINATOR) and not user_has_role(
            request.user,
            ROLE_ADMINISTRATOR,
            ROLE_SECRETARY,
        ):
            career_ids = coordinator_career_ids(request.user)
            course_sections = course_sections.filter(offer__career_id__in=career_ids)
            enrollments = enrollments.filter(career_id__in=career_ids)

        course_enrollments = CourseEnrollment.objects.filter(
            course_section__in=course_sections,
            status=CourseEnrollmentStatus.ENROLLED,
        )
        teaching_assignments = TeachingAssignment.objects.filter(
            course_section__in=course_sections,
            status=TeachingAssignmentStatus.ACTIVE,
        )

        return Response(
            {
                "period": {
                    "id": period.id,
                    "code": period.code,
                    "name": period.name,
                },
                "counts": {
                    "students": enrollments.values("student_id").distinct().count(),
                    "teachers": teaching_assignments.values("teacher_id")
                    .distinct()
                    .count(),
                    "courses": course_sections.count(),
                    "enrollments": course_enrollments.count(),
                },
            }
        )

    def _get_period(self, request):
        period_param = request.query_params.get("period")
        if period_param:
            lookup = {"code": period_param}
            if period_param.isdigit():
                lookup = {"id": int(period_param)}
            return get_object_or_404(AcademicPeriod, **lookup)

        current_period = AcademicPeriod.objects.filter(is_current=True).first()
        if current_period:
            return current_period
        latest_period = AcademicPeriod.objects.order_by("-start_date").first()
        if latest_period:
            return latest_period
        raise Http404("No existen periodos academicos.")
