from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import HttpResponse
from django.utils.html import escape
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from .models import Syllabus
from .selectors import (
    user_can_create_syllabus_records,
    user_can_view_syllabus_records,
    visible_achievement_levels_for_user,
    visible_bibliography_for_user,
    visible_competencies_for_user,
    visible_criteria_for_user,
    visible_learning_outcomes_for_user,
    visible_syllabi_for_user,
    visible_weekly_plans_for_user,
)
from .serializers import (
    SyllabusAchievementLevelSerializer,
    SyllabusBibliographySerializer,
    SyllabusCompetencySerializer,
    SyllabusCriterionSerializer,
    SyllabusLearningOutcomeSerializer,
    SyllabusSerializer,
    SyllabusWeeklyPlanSerializer,
)
from .services import (
    approve_syllabus,
    finalize_syllabus,
    model_validation_error_to_serializer_error,
    observe_syllabus,
    reopen_syllabus,
    submit_syllabus,
    syllabus_print_context,
    upload_signed_syllabus,
    user_can_approve_syllabus,
    user_can_edit_syllabus,
    user_is_assigned_teacher,
)


class CanReadOrManageSyllabus(BasePermission):
    def has_permission(self, request, view):
        if not getattr(request.user, "is_authenticated", False):
            return False
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return user_can_view_syllabus_records(request.user)
        if getattr(view, "action", "") in {
            "finalize",
            "submit",
            "approve",
            "observe",
            "reopen",
            "upload_signed_file",
        }:
            return user_can_view_syllabus_records(request.user)
        return user_can_create_syllabus_records(request.user)


class SyllabusViewSet(viewsets.ModelViewSet):
    serializer_class = SyllabusSerializer
    permission_classes = [CanReadOrManageSyllabus]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = (
        "course_section__subject__code",
        "course_section__subject__name",
        "course_section__offer__period__code",
        "lead_teacher__person__first_name",
        "lead_teacher__person__last_name",
        "status",
    )
    ordering_fields = ("created_at", "updated_at", "status", "version")

    def get_queryset(self):
        return visible_syllabi_for_user(self.request.user)

    def perform_create(self, serializer):
        instance = Syllabus(**serializer.validated_data)
        if not user_can_edit_syllabus(self.request.user, instance):
            raise PermissionDenied("No tiene permisos para crear este silabo.")
        serializer.save()

    def perform_update(self, serializer):
        if not user_can_edit_syllabus(self.request.user, serializer.instance):
            raise PermissionDenied("No tiene permisos para editar este silabo.")
        serializer.save()

    def perform_destroy(self, instance):
        if not user_can_approve_syllabus(self.request.user, instance):
            raise PermissionDenied("No tiene permisos para eliminar este silabo.")
        instance.delete()

    def _workflow_response(self, service, *args, **kwargs):
        syllabus = self.get_object()
        try:
            updated = service(
                syllabus,
                *args,
                user=self.request.user,
                request=self.request,
                **kwargs,
            )
        except DjangoValidationError as exc:
            return Response(
                model_validation_error_to_serializer_error(exc),
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(self.get_serializer(updated).data)

    @action(detail=True, methods=["post"])
    def finalize(self, request, pk=None):
        syllabus = self.get_object()
        if not user_can_edit_syllabus(request.user, syllabus):
            raise PermissionDenied("No tiene permisos para finalizar este silabo.")
        return self._workflow_response(finalize_syllabus)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        syllabus = self.get_object()
        if not user_is_assigned_teacher(request.user, syllabus):
            raise PermissionDenied("No tiene permisos para enviar este silabo.")
        return self._workflow_response(submit_syllabus)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        return self._workflow_response(approve_syllabus)

    @action(detail=True, methods=["post"])
    def observe(self, request, pk=None):
        reason = request.data.get("reason", "")
        return self._workflow_response(observe_syllabus, reason=reason)

    @action(detail=True, methods=["post"])
    def reopen(self, request, pk=None):
        reason = request.data.get("reason", "")
        return self._workflow_response(reopen_syllabus, reason=reason)

    @action(
        detail=True,
        methods=["post"],
        parser_classes=[MultiPartParser, FormParser],
        url_path="upload-signed-file",
    )
    def upload_signed_file(self, request, pk=None):
        signed_file = request.FILES.get("signed_file")
        if signed_file is None:
            return Response(
                {"signed_file": ["Adjunte un archivo PDF."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return self._workflow_response(upload_signed_syllabus, signed_file=signed_file)

    @action(detail=True, methods=["get"], url_path="printable")
    def printable(self, request, pk=None):
        context = syllabus_print_context(self.get_object())
        return HttpResponse(_render_syllabus_html(context), content_type="text/html")


class SyllabusChildViewSet(viewsets.ModelViewSet):
    permission_classes = [CanReadOrManageSyllabus]
    filter_backends = [OrderingFilter]
    ordering_fields = ("order", "created_at", "updated_at")

    def _syllabus_from_validated_data(self, validated_data):
        if "syllabus" in validated_data:
            return validated_data["syllabus"]
        if "learning_outcome" in validated_data:
            return validated_data["learning_outcome"].syllabus
        if "criterion" in validated_data:
            return validated_data["criterion"].syllabus
        return None

    def _ensure_can_edit(self, syllabus):
        if syllabus is None or not user_can_edit_syllabus(self.request.user, syllabus):
            raise PermissionDenied("No tiene permisos para editar este silabo.")

    def perform_create(self, serializer):
        self._ensure_can_edit(
            self._syllabus_from_validated_data(serializer.validated_data)
        )
        serializer.save()

    def perform_update(self, serializer):
        self._ensure_can_edit(serializer.instance.syllabus)
        serializer.save()

    def perform_destroy(self, instance):
        self._ensure_can_edit(instance.syllabus)
        instance.delete()


class SyllabusCompetencyViewSet(SyllabusChildViewSet):
    serializer_class = SyllabusCompetencySerializer

    def get_queryset(self):
        return visible_competencies_for_user(self.request.user)


class SyllabusLearningOutcomeViewSet(SyllabusChildViewSet):
    serializer_class = SyllabusLearningOutcomeSerializer

    def get_queryset(self):
        return visible_learning_outcomes_for_user(self.request.user)


class SyllabusCriterionViewSet(SyllabusChildViewSet):
    serializer_class = SyllabusCriterionSerializer

    def get_queryset(self):
        return visible_criteria_for_user(self.request.user)


class SyllabusAchievementLevelViewSet(SyllabusChildViewSet):
    serializer_class = SyllabusAchievementLevelSerializer

    def get_queryset(self):
        return visible_achievement_levels_for_user(self.request.user)

    def perform_update(self, serializer):
        self._ensure_can_edit(serializer.instance.criterion.syllabus)
        serializer.save()

    def perform_destroy(self, instance):
        self._ensure_can_edit(instance.criterion.syllabus)
        instance.delete()


class SyllabusBibliographyViewSet(SyllabusChildViewSet):
    serializer_class = SyllabusBibliographySerializer

    def get_queryset(self):
        return visible_bibliography_for_user(self.request.user)


class SyllabusWeeklyPlanViewSet(SyllabusChildViewSet):
    serializer_class = SyllabusWeeklyPlanSerializer

    def get_queryset(self):
        return visible_weekly_plans_for_user(self.request.user)


def _render_syllabus_html(context):
    syllabus = context["syllabus"]
    course = context["course"]
    subject = context["subject"]
    rows = [
        "<!doctype html>",
        "<html lang='es'><head><meta charset='utf-8'>",
        "<title>Silabo imprimible</title>",
        "<style>body{font-family:Arial,sans-serif;margin:32px;color:#111827;}",
        "h1{font-size:24px;margin:0 0 8px;} h2{font-size:18px;margin-top:24px;}",
        "table{width:100%;border-collapse:collapse;margin-top:8px;}",
        "th,td{border:1px solid #d1d5db;padding:8px;text-align:left;",
        "vertical-align:top;}",
        ".muted{color:#4b5563;} .small{font-size:12px;}</style></head><body>",
        f"<h1>Silabo - {escape(subject.name)}</h1>",
        (
            f"<p class='muted'>{escape(subject.code)} | "
            f"Paralelo {escape(course.parallel)} | "
            f"{escape(course.offer.period.code)}</p>"
        ),
        "<h2>Datos informativos</h2>",
        "<table><tbody>",
        f"<tr><th>Carrera</th><td>{escape(course.offer.career.name)}</td></tr>",
        (
            "<tr><th>Docente titular</th><td>"
            f"{escape(syllabus.lead_teacher.person.full_name)}</td></tr>"
        ),
        f"<tr><th>Version</th><td>{escape(syllabus.get_version_display())}</td></tr>",
        f"<tr><th>Estado</th><td>{escape(syllabus.get_status_display())}</td></tr>",
        "</tbody></table>",
        "<h2>Descripcion</h2>",
        f"<p>{escape(syllabus.subject_description)}</p>",
        "<h2>Metodologia</h2>",
        f"<p>{escape(syllabus.methodology)}</p>",
        "<h2>Competencias</h2><ul>",
    ]
    for competency in context["competencies"]:
        rows.append(
            f"<li><strong>{escape(competency.get_competency_type_display())}:</strong> "
            f"{escape(competency.text)}</li>"
        )
    rows.append("</ul><h2>Resultados y rubricas</h2>")
    for outcome in context["learning_outcomes"]:
        rows.append(
            f"<h3>{escape(outcome.get_outcome_type_display())} {outcome.order}</h3>"
        )
        rows.append(f"<p>{escape(outcome.text)}</p>")
        rows.append(
            "<table><thead><tr><th>Criterio</th><th>Peso</th>"
            "<th>Niveles</th></tr></thead><tbody>"
        )
        for criterion in outcome.criteria.all():
            levels = ", ".join(
                f"{level.level}: {level.description}"
                for level in criterion.achievement_levels.all()
            )
            rows.append(
                f"<tr><td>{escape(criterion.name)}</td><td>{criterion.weight}%</td>"
                f"<td>{escape(levels)}</td></tr>"
            )
        rows.append("</tbody></table>")
    rows.append(
        "<h2>Planificacion semanal</h2><table><thead><tr>"
        "<th>Semana</th><th>RA</th><th>Experiencias</th><th>Horas</th>"
        "</tr></thead><tbody>"
    )
    for plan in context["weekly_plan"]:
        hours = plan.contact_hours + plan.practical_hours + plan.autonomous_hours
        strategies = " | ".join(
            item
            for item in [
                plan.contact_strategy,
                plan.practical_strategy,
                plan.autonomous_strategy,
            ]
            if item
        )
        rows.append(
            f"<tr><td>{escape(str(plan))}</td>"
            f"<td>{escape(str(plan.learning_outcome))}</td>"
            f"<td>{escape(strategies)}</td><td>{hours}</td></tr>"
        )
    rows.append("</tbody></table><h2>Bibliografia</h2><ul>")
    for item in context["bibliography"]:
        rows.append(
            f"<li><strong>{escape(item.get_bibliography_type_display())}:</strong> "
            f"{escape(item.apa_reference)}</li>"
        )
    rows.append(
        "</ul><h2>Firmas</h2><p class='small'>"
        "Docente titular | Coordinacion | Direccion academica</p>"
    )
    rows.append("</body></html>")
    return "".join(rows)
