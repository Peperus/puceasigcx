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
from apps.grading.models import GradeCalculationSnapshot
from apps.grading.selectors import (
    user_can_export_grade_reports,
    visible_gradebooks_for_reports,
)
from apps.grading.serializers import GradeCalculationSnapshotSerializer

from .selectors import (
    MVP_REPORT_DEFINITIONS,
    mvp_report_payload,
    resolve_report_filters,
    user_can_view_mvp_reports,
)
from .services import grade_export_response, tabular_export_response


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


class CanViewMvpReports(BasePermission):
    def has_permission(self, request, view):
        return bool(
            getattr(request.user, "is_authenticated", False)
            and user_can_view_mvp_reports(request.user)
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


class MvpReportView(APIView):
    permission_classes = [CanViewMvpReports]

    def get(self, request, report_type):
        definition = MVP_REPORT_DEFINITIONS.get(report_type)
        if definition is None:
            return Response(
                {
                    "report_type": (
                        "Reporte no soportado. Use students, teachers, courses, "
                        "syllabi o grades."
                    )
                },
                status=404,
            )
        filters = resolve_report_filters(request.query_params)
        for optional_filter in ("status", "grading_model"):
            if request.query_params.get(optional_filter):
                filters[optional_filter] = request.query_params[optional_filter]
        data, rows = mvp_report_payload(
            report_type=report_type,
            user=request.user,
            filters=filters,
        )
        export_format = request.query_params.get("file_format")
        if export_format:
            export_format = export_format.lower()
            if export_format not in {"csv", "xlsx"}:
                return Response(
                    {"file_format": "Formato no soportado. Use csv o xlsx."},
                    status=400,
                )
            return tabular_export_response(
                title=definition["title"],
                headers=definition["headers"],
                rows=rows,
                export_format=export_format,
                user=request.user,
                filters=filters,
                request=request,
            )
        return Response(
            {
                "report_type": report_type,
                "filters": filters,
                "count": len(data),
                "results": data,
            }
        )


class CanViewGradeReports(BasePermission):
    def has_permission(self, request, view):
        return bool(
            getattr(request.user, "is_authenticated", False)
            and user_can_export_grade_reports(request.user)
        )


class AcademicGradeQueryView(APIView):
    permission_classes = [CanViewGradeReports]

    def get(self, request):
        snapshots = self._queryset(request)
        serializer = GradeCalculationSnapshotSerializer(snapshots, many=True)
        return Response(serializer.data)

    def _queryset(self, request):
        gradebooks = visible_gradebooks_for_reports(request.user)
        snapshots = GradeCalculationSnapshot.objects.filter(
            is_current=True,
            gradebook__in=gradebooks,
        ).select_related(
            "gradebook",
            "gradebook__course_section",
            "gradebook__course_section__subject",
            "gradebook__course_section__offer",
            "gradebook__course_section__offer__period",
            "gradebook__course_section__offer__career",
            "course_enrollment",
            "course_enrollment__enrollment",
            "course_enrollment__enrollment__student",
            "course_enrollment__enrollment__student__person",
        )
        filters = request.query_params
        if filters.get("period"):
            snapshots = snapshots.filter(
                gradebook__course_section__offer__period__code=filters["period"]
            )
        if filters.get("career"):
            snapshots = snapshots.filter(
                gradebook__course_section__offer__career_id=filters["career"]
            )
        if filters.get("course"):
            snapshots = snapshots.filter(gradebook__course_section_id=filters["course"])
        if filters.get("gradebook"):
            snapshots = snapshots.filter(gradebook_id=filters["gradebook"])
        if filters.get("teacher"):
            snapshots = snapshots.filter(
                gradebook__course_section__teaching_assignments__teacher_id=filters[
                    "teacher"
                ],
                gradebook__course_section__teaching_assignments__status=(
                    TeachingAssignmentStatus.ACTIVE
                ),
            )
        if filters.get("student"):
            snapshots = snapshots.filter(
                course_enrollment__enrollment__student_id=filters["student"]
            )
        if filters.get("grading_model"):
            snapshots = snapshots.filter(grading_model=filters["grading_model"])
        status = filters.get("status") or filters.get("result")
        if status:
            snapshots = snapshots.filter(final_status=status)
        return snapshots.distinct().order_by(
            "gradebook__course_section__subject__code",
            "course_enrollment__enrollment__student__student_code",
        )


class GradeExportView(AcademicGradeQueryView):
    def get(self, request):
        export_format = request.query_params.get(
            "file_format",
            request.query_params.get("format", "csv"),
        ).lower()
        if export_format not in {"csv", "xlsx"}:
            return Response(
                {"format": "Formato no soportado. Use csv o xlsx."},
                status=400,
            )
        snapshots = list(self._queryset(request))
        return grade_export_response(
            snapshots=snapshots,
            export_format=export_format,
            user=request.user,
            filters=dict(request.query_params),
            request=request,
        )
