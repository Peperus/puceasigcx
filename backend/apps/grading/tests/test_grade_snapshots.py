import pytest

from apps.grading.models import GradeCalculationSnapshot, GradeFinalStatus, GradingModel
from apps.grading.services import recalculate_gradebook, save_grade_record
from apps.grading.tests.factories import (
    add_s1_s2_structure,
    make_course_enrollment,
    make_gradebook,
)


@pytest.mark.django_db
def test_recalculate_gradebook_persists_current_snapshot_and_keeps_history():
    gradebook = make_gradebook(code="SNAP", grading_model=GradingModel.S1)
    course_enrollment = make_course_enrollment(
        code="SNAP",
        course_section=gradebook.course_section,
    )
    items = add_s1_s2_structure(gradebook)
    for item in items:
        save_grade_record(
            gradebook=gradebook,
            course_enrollment=course_enrollment,
            grade_item=item["activity"],
            score=40,
        )

    snapshots = recalculate_gradebook(
        gradebook,
        course_enrollments=[course_enrollment],
        source="test",
    )

    assert len(snapshots) == 1
    assert snapshots[0].is_current is True
    assert snapshots[0].final_status == GradeFinalStatus.APPROVED
    assert snapshots[0].payload["grading_model"] == GradingModel.S1

    save_grade_record(
        gradebook=gradebook,
        course_enrollment=course_enrollment,
        grade_item=items[0]["activity"],
        score=30,
        reason="Correccion sintetica",
    )
    recalculate_gradebook(
        gradebook,
        course_enrollments=[course_enrollment],
        source="test",
    )

    assert (
        GradeCalculationSnapshot.objects.filter(
            gradebook=gradebook,
            course_enrollment=course_enrollment,
        ).count()
        == 2
    )
    assert (
        GradeCalculationSnapshot.objects.filter(
            gradebook=gradebook,
            course_enrollment=course_enrollment,
            is_current=True,
        ).count()
        == 1
    )
