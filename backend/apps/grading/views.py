from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.enrollment.models import CourseEnrollmentStatus
from apps.enrollment.services import model_validation_error_to_serializer_error

from .models import (
    Gradebook,
    GradeCalculationSnapshot,
    GradeItem,
    GradeItemType,
)
from .selectors import (
    gradebook_course_enrollments,
    student_course_enrollments_for_user,
    teacher_gradebooks_for_user,
    user_can_edit_gradebook,
    user_can_manage_gradebook_closure,
)
from .serializers import (
    BulkGradeEntryRowSerializer,
    CourseEnrollmentGradeStudentSerializer,
    GradebookCourseSerializer,
    GradeCalculationSnapshotSerializer,
    GradeEntrySerializer,
    GradeRecordSerializer,
    RACriterionBulkEntrySerializer,
    S3FinalEvaluationEntrySerializer,
    S3PartialEntrySerializer,
    grade_item_is_valid_for_ra_criterion,
    grade_item_tree_data,
)
from .services import (
    close_gradebook,
    recalculate_gradebook,
    reopen_gradebook,
    save_grade_record,
)


def _as_serializer_error(exc):
    return model_validation_error_to_serializer_error(exc)


def _raise_service_error(exc):
    raise serializers.ValidationError(_as_serializer_error(exc)) from exc


class IsTeacherGradeUser(BasePermission):
    def has_permission(self, request, view):
        return bool(getattr(request.user, "is_authenticated", False))


class CanManageGradebookClosure(BasePermission):
    def has_permission(self, request, view):
        return bool(
            getattr(request.user, "is_authenticated", False)
            and user_can_manage_gradebook_closure(request.user)
        )


class TeacherGradebookViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GradebookCourseSerializer
    permission_classes = [IsTeacherGradeUser]

    def get_queryset(self):
        return teacher_gradebooks_for_user(self.request.user)

    def _get_gradebook(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])

    def _ensure_editable(self, gradebook):
        if not user_can_edit_gradebook(self.request.user, gradebook):
            raise serializers.ValidationError(
                {"gradebook": ("El libro debe estar abierto y asignado al docente.")}
            )

    def _get_enrollment(self, gradebook, enrollment_id):
        return get_object_or_404(
            gradebook_course_enrollments(gradebook),
            pk=enrollment_id,
            status=CourseEnrollmentStatus.ENROLLED,
        )

    def _get_item(self, gradebook, item_id):
        return get_object_or_404(GradeItem, pk=item_id, gradebook=gradebook)

    @action(detail=True, methods=["get"])
    def students(self, request, pk=None):
        gradebook = self._get_gradebook()
        serializer = CourseEnrollmentGradeStudentSerializer(
            gradebook_course_enrollments(gradebook),
            many=True,
        )
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def structure(self, request, pk=None):
        gradebook = self.get_queryset().prefetch_related("items")
        gradebook = get_object_or_404(gradebook, pk=self.kwargs["pk"])
        return Response(
            {
                "gradebook": GradebookCourseSerializer(gradebook).data,
                "items": grade_item_tree_data(gradebook),
            }
        )

    @action(detail=True, methods=["post"], url_path="record")
    def record(self, request, pk=None):
        gradebook = self._get_gradebook()
        self._ensure_editable(gradebook)
        serializer = GradeEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        enrollment = self._get_enrollment(gradebook, data["course_enrollment"])
        grade_item = self._get_item(gradebook, data["grade_item"])

        try:
            record = save_grade_record(
                gradebook=gradebook,
                course_enrollment=enrollment,
                grade_item=grade_item,
                score=data["score"],
                user=request.user,
                reason=data.get("reason", ""),
                request=request,
            )
            snapshot = recalculate_gradebook(
                gradebook,
                course_enrollments=[enrollment],
                user=request.user,
                source="teacher_grade_entry",
                request=request,
                allow_incomplete=True,
            )[0]
        except DjangoValidationError as exc:
            _raise_service_error(exc)

        return Response(
            {
                "record": GradeRecordSerializer(record).data,
                "snapshot": GradeCalculationSnapshotSerializer(snapshot).data,
            }
        )

    @action(detail=True, methods=["post"], url_path="ra-criterion-entry")
    def ra_criterion_entry(self, request, pk=None):
        gradebook = self._get_gradebook()
        self._ensure_editable(gradebook)
        serializer = RACriterionBulkEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        outcome = self._get_item(gradebook, data["learning_outcome"])
        criterion = self._get_item(gradebook, data["criterion"])
        grade_item = self._resolve_ra_grade_item(gradebook, criterion, data)
        if not grade_item_is_valid_for_ra_criterion(
            outcome=outcome,
            criterion=criterion,
            grade_item=grade_item,
        ):
            raise serializers.ValidationError(
                {"grade_item": "El item no pertenece al RA y criterio indicados."}
            )
        return self._save_bulk_entries(
            gradebook,
            grade_item=grade_item,
            entries=data["entries"],
            source="ra_criterion_entry",
        )

    def _resolve_ra_grade_item(self, gradebook, criterion, data):
        if data.get("grade_item"):
            return self._get_item(gradebook, data["grade_item"])
        activity_ids = list(
            criterion.children.filter(item_type=GradeItemType.ACTIVITY).values_list(
                "id",
                flat=True,
            )
        )
        if len(activity_ids) == 1:
            return self._get_item(gradebook, activity_ids[0])
        return criterion

    @action(detail=True, methods=["post"], url_path="s3-partial-entry")
    def s3_partial_entry(self, request, pk=None):
        gradebook = self._get_gradebook()
        self._ensure_editable(gradebook)
        serializer = S3PartialEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        partial = self._get_item(gradebook, serializer.validated_data["partial"])
        if partial.item_type != GradeItemType.PARTIAL:
            raise serializers.ValidationError({"partial": "El item no es un parcial."})

        entries = serializer.validated_data["entries"]
        saved_records = []
        enrollments = []
        errors = []
        with transaction.atomic():
            for index, entry in enumerate(entries):
                enrollment_id = entry.get("course_enrollment")
                if not enrollment_id:
                    errors.append({"index": index, "course_enrollment": "Requerido."})
                    continue
                enrollment = self._get_enrollment(gradebook, enrollment_id)
                row_records = self._s3_records_for_entry(partial, entry)
                if not row_records:
                    errors.append(
                        {"index": index, "scores": "No hay notas para guardar."}
                    )
                    continue
                try:
                    for item, score in row_records:
                        saved_records.append(
                            save_grade_record(
                                gradebook=gradebook,
                                course_enrollment=enrollment,
                                grade_item=item,
                                score=score,
                                user=self.request.user,
                                reason=entry.get("reason", ""),
                                request=self.request,
                            )
                        )
                    enrollments.append(enrollment)
                except DjangoValidationError as exc:
                    errors.append({"index": index, "errors": _as_serializer_error(exc)})
            if errors:
                raise serializers.ValidationError({"entries": errors})
            snapshots = recalculate_gradebook(
                gradebook,
                course_enrollments=enrollments,
                user=self.request.user,
                source="s3_partial_entry",
                request=self.request,
                allow_incomplete=True,
            )
        return Response(
            {
                "records": GradeRecordSerializer(saved_records, many=True).data,
                "snapshots": GradeCalculationSnapshotSerializer(
                    snapshots,
                    many=True,
                ).data,
            }
        )

    def _s3_records_for_entry(self, partial, entry):
        score_map = self._score_map(partial, entry)
        records = []
        for item in partial.children.all():
            if item.pk in score_map:
                records.append((item, score_map[item.pk]))
        return records

    def _score_map(self, partial, entry):
        score_map = {}
        for key in ("practice_scores", "scores"):
            raw_scores = entry.get(key) or {}
            if isinstance(raw_scores, dict):
                score_map.update(
                    {int(item_id): score for item_id, score in raw_scores.items()}
                )
            if isinstance(raw_scores, list):
                score_map.update(
                    {
                        int(item["grade_item"]): item["score"]
                        for item in raw_scores
                        if "grade_item" in item and "score" in item
                    }
                )
        if "evaluation_item" in entry and "evaluation_score" in entry:
            score_map[int(entry["evaluation_item"])] = entry["evaluation_score"]
        elif "evaluation_score" in entry:
            evaluation_items = [
                item
                for item in partial.children.all()
                if item.item_type == GradeItemType.EVALUATION
            ]
            if len(evaluation_items) == 1:
                score_map[evaluation_items[0].pk] = entry["evaluation_score"]
        return score_map

    @action(detail=True, methods=["post"], url_path="s3-final-evaluation")
    def s3_final_evaluation(self, request, pk=None):
        gradebook = self._get_gradebook()
        self._ensure_editable(gradebook)
        serializer = S3FinalEvaluationEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = self._get_item(gradebook, serializer.validated_data["final_evaluation"])
        if item.item_type != GradeItemType.FINAL_EVALUATION:
            raise serializers.ValidationError(
                {"final_evaluation": "El item no es evaluacion final."}
            )
        return self._save_bulk_entries(
            gradebook,
            grade_item=item,
            entries=serializer.validated_data["entries"],
            source="s3_final_evaluation",
        )

    def _save_bulk_entries(self, gradebook, *, grade_item, entries, source):
        saved_records = []
        enrollments = []
        errors = []
        with transaction.atomic():
            for index, entry in enumerate(entries):
                row_serializer = BulkGradeEntryRowSerializer(data=entry)
                if not row_serializer.is_valid():
                    errors.append({"index": index, "errors": row_serializer.errors})
                    continue
                data = row_serializer.validated_data
                try:
                    enrollment = (
                        gradebook_course_enrollments(gradebook)
                        .filter(
                            pk=data["course_enrollment"],
                            status=CourseEnrollmentStatus.ENROLLED,
                        )
                        .first()
                    )
                    if enrollment is None:
                        errors.append(
                            {
                                "index": index,
                                "course_enrollment": (
                                    "La matricula no pertenece al curso."
                                ),
                            }
                        )
                        continue
                    saved_records.append(
                        save_grade_record(
                            gradebook=gradebook,
                            course_enrollment=enrollment,
                            grade_item=grade_item,
                            score=data["score"],
                            user=self.request.user,
                            reason=data.get("reason", ""),
                            request=self.request,
                        )
                    )
                    enrollments.append(enrollment)
                except DjangoValidationError as exc:
                    errors.append({"index": index, "errors": _as_serializer_error(exc)})
            if errors:
                raise serializers.ValidationError({"entries": errors})
            snapshots = recalculate_gradebook(
                gradebook,
                course_enrollments=enrollments,
                user=self.request.user,
                source=source,
                request=self.request,
                allow_incomplete=True,
            )
        return Response(
            {
                "records": GradeRecordSerializer(saved_records, many=True).data,
                "snapshots": GradeCalculationSnapshotSerializer(
                    snapshots,
                    many=True,
                ).data,
            }
        )


class GradebookClosureViewSet(viewsets.GenericViewSet):
    queryset = Gradebook.objects.select_related("course_section")
    serializer_class = GradebookCourseSerializer
    permission_classes = [CanManageGradebookClosure]

    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        gradebook = self.get_object()
        try:
            gradebook = close_gradebook(
                gradebook,
                user=request.user,
                request=request,
                allow_incomplete=bool(request.data.get("allow_incomplete", False)),
            )
        except DjangoValidationError as exc:
            _raise_service_error(exc)
        return Response(GradebookCourseSerializer(gradebook).data)

    @action(detail=True, methods=["post"])
    def reopen(self, request, pk=None):
        gradebook = self.get_object()
        try:
            gradebook = reopen_gradebook(
                gradebook,
                reason=request.data.get("reason", ""),
                user=request.user,
                request=request,
            )
        except DjangoValidationError as exc:
            _raise_service_error(exc)
        return Response(GradebookCourseSerializer(gradebook).data)


class StudentGradesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        course_enrollments = student_course_enrollments_for_user(request.user)
        data = []
        for course_enrollment in course_enrollments:
            gradebook = course_enrollment.course_section.gradebook
            snapshot = (
                GradeCalculationSnapshot.objects.filter(
                    gradebook=gradebook,
                    course_enrollment=course_enrollment,
                    is_current=True,
                )
                .select_related(
                    "gradebook",
                    "gradebook__course_section",
                    "gradebook__course_section__subject",
                    "gradebook__course_section__offer",
                    "gradebook__course_section__offer__period",
                    "course_enrollment",
                    "course_enrollment__enrollment",
                    "course_enrollment__enrollment__student",
                    "course_enrollment__enrollment__student__person",
                )
                .first()
            )
            data.append(
                {
                    "course_enrollment_id": course_enrollment.pk,
                    "gradebook_id": gradebook.pk,
                    "period_code": gradebook.course_section.offer.period.code,
                    "career_name": gradebook.course_section.offer.career.name,
                    "subject_code": gradebook.course_section.subject.code,
                    "subject_name": gradebook.course_section.subject.name,
                    "parallel": gradebook.course_section.parallel,
                    "grading_model": gradebook.grading_model,
                    "gradebook_status": gradebook.status,
                    "snapshot": (
                        GradeCalculationSnapshotSerializer(snapshot).data
                        if snapshot
                        else None
                    ),
                }
            )
        return Response(data)
