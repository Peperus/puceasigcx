"""Serializers for grading API resources."""

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.enrollment.services import model_validation_error_to_serializer_error

from .models import (
    Gradebook,
    GradeCalculationSnapshot,
    GradeItem,
    GradeItemType,
    StudentGradeRecord,
)
from .services import validate_score


class GradebookCourseSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(source="course_section_id", read_only=True)
    subject_code = serializers.CharField(
        source="course_section.subject.code",
        read_only=True,
    )
    subject_name = serializers.CharField(
        source="course_section.subject.name",
        read_only=True,
    )
    parallel = serializers.CharField(
        source="course_section.parallel",
        read_only=True,
    )
    period_code = serializers.CharField(
        source="course_section.offer.period.code",
        read_only=True,
    )
    career_name = serializers.CharField(
        source="course_section.offer.career.name",
        read_only=True,
    )
    enrolled_count = serializers.IntegerField(
        source="course_section.enrolled_count",
        read_only=True,
    )

    class Meta:
        model = Gradebook
        fields = (
            "id",
            "course_id",
            "subject_code",
            "subject_name",
            "parallel",
            "period_code",
            "career_name",
            "grading_model",
            "status",
            "enrolled_count",
            "opened_at",
            "closed_at",
        )


class CourseEnrollmentGradeStudentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    student_id = serializers.IntegerField(source="enrollment.student_id")
    student_code = serializers.CharField(source="enrollment.student.student_code")
    student_name = serializers.CharField(source="enrollment.student.person.full_name")
    status = serializers.CharField()


class GradeItemSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = GradeItem
        fields = (
            "id",
            "parent",
            "item_type",
            "name",
            "order",
            "weight",
            "max_score",
            "children",
        )

    def get_children(self, obj):
        children_by_parent = self.context.get("children_by_parent", {})
        return GradeItemSerializer(
            children_by_parent.get(obj.pk, []),
            many=True,
            context=self.context,
        ).data


class GradeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGradeRecord
        fields = (
            "id",
            "gradebook",
            "course_enrollment",
            "grade_item",
            "score",
            "status",
            "reason",
            "created_at",
            "updated_at",
        )


class GradeEntrySerializer(serializers.Serializer):
    course_enrollment = serializers.IntegerField()
    grade_item = serializers.IntegerField()
    score = serializers.DecimalField(max_digits=5, decimal_places=2)
    reason = serializers.CharField(required=False, allow_blank=True)

    def validate_score(self, value):
        try:
            return validate_score(value)
        except DjangoValidationError as exc:
            errors = model_validation_error_to_serializer_error(exc)
            raise serializers.ValidationError(
                errors.get("score", exc.messages)
            ) from exc


class BulkGradeEntryRowSerializer(serializers.Serializer):
    course_enrollment = serializers.IntegerField()
    score = serializers.DecimalField(max_digits=5, decimal_places=2)
    reason = serializers.CharField(required=False, allow_blank=True)

    def validate_score(self, value):
        try:
            return validate_score(value)
        except DjangoValidationError as exc:
            errors = model_validation_error_to_serializer_error(exc)
            raise serializers.ValidationError(
                errors.get("score", exc.messages)
            ) from exc


class RACriterionBulkEntrySerializer(serializers.Serializer):
    learning_outcome = serializers.IntegerField()
    criterion = serializers.IntegerField()
    grade_item = serializers.IntegerField(required=False)
    entries = BulkGradeEntryRowSerializer(many=True)


class S3PartialEntrySerializer(serializers.Serializer):
    partial = serializers.IntegerField()
    entries = serializers.ListField(child=serializers.DictField(), allow_empty=False)


class S3FinalEvaluationEntrySerializer(serializers.Serializer):
    final_evaluation = serializers.IntegerField()
    entries = BulkGradeEntryRowSerializer(many=True)


class GradeCalculationSnapshotSerializer(serializers.ModelSerializer):
    student_code = serializers.CharField(
        source="course_enrollment.enrollment.student.student_code",
        read_only=True,
    )
    student_name = serializers.CharField(
        source="course_enrollment.enrollment.student.person.full_name",
        read_only=True,
    )
    subject_code = serializers.CharField(
        source="gradebook.course_section.subject.code",
        read_only=True,
    )
    subject_name = serializers.CharField(
        source="gradebook.course_section.subject.name",
        read_only=True,
    )
    period_code = serializers.CharField(
        source="gradebook.course_section.offer.period.code",
        read_only=True,
    )

    class Meta:
        model = GradeCalculationSnapshot
        fields = (
            "id",
            "gradebook",
            "course_enrollment",
            "student_code",
            "student_name",
            "subject_code",
            "subject_name",
            "period_code",
            "grading_model",
            "final_score",
            "final_letter",
            "final_status",
            "failed_learning_outcomes_count",
            "recovery_required",
            "payload",
            "source",
            "calculated_at",
        )


class StudentGradeCourseSerializer(serializers.Serializer):
    course_enrollment_id = serializers.IntegerField()
    gradebook_id = serializers.IntegerField()
    period_code = serializers.CharField()
    career_name = serializers.CharField()
    subject_code = serializers.CharField()
    subject_name = serializers.CharField()
    parallel = serializers.CharField()
    grading_model = serializers.CharField()
    gradebook_status = serializers.CharField()
    snapshot = GradeCalculationSnapshotSerializer(allow_null=True)


def grade_item_tree_data(gradebook):
    children_by_parent = {}
    for item in gradebook.items.all():
        children_by_parent.setdefault(item.parent_id, []).append(item)
    roots = children_by_parent.get(None, [])
    return GradeItemSerializer(
        roots,
        many=True,
        context={"children_by_parent": children_by_parent},
    ).data


def grade_item_is_valid_for_ra_criterion(*, outcome, criterion, grade_item):
    return bool(
        outcome.item_type == GradeItemType.LEARNING_OUTCOME
        and criterion.parent_id == outcome.pk
        and criterion.item_type == GradeItemType.CRITERION
        and grade_item.gradebook_id == outcome.gradebook_id
        and grade_item.item_type in {GradeItemType.CRITERION, GradeItemType.ACTIVITY}
        and (grade_item.pk == criterion.pk or grade_item.parent_id == criterion.pk)
    )
