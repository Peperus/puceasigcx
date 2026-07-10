import pytest
from rest_framework.test import APIClient

from apps.grading.models import GradebookStatus, GradeFinalStatus, GradingModel
from apps.grading.services import (
    open_gradebook,
    recalculate_gradebook,
    save_grade_record,
)
from apps.grading.tests.factories import (
    add_s1_s2_structure,
    make_course_enrollment,
    make_gradebook,
)
from apps.people.tests.factories import make_user


@pytest.mark.django_db
def test_student_sees_only_own_visible_grades():
    gradebook = make_gradebook(code="S7T4A", grading_model=GradingModel.S1)
    open_gradebook(gradebook)
    items = add_s1_s2_structure(gradebook)
    course_enrollment = make_course_enrollment(
        code="S7T4A",
        course_section=gradebook.course_section,
    )
    user = make_user("estudiante-s7t4@example.edu", "USR-S7T4", "Estudiante")
    person = course_enrollment.enrollment.student.person
    person.user = user
    person.save()
    for item in items:
        save_grade_record(
            gradebook=gradebook,
            course_enrollment=course_enrollment,
            grade_item=item["activity"],
            score=40,
        )
    recalculate_gradebook(gradebook, course_enrollments=[course_enrollment])

    other_gradebook = make_gradebook(code="S7T4B", grading_model=GradingModel.S1)
    open_gradebook(other_gradebook)
    other_items = add_s1_s2_structure(other_gradebook)
    other_enrollment = make_course_enrollment(
        code="S7T4B",
        course_section=other_gradebook.course_section,
    )
    for item in other_items:
        save_grade_record(
            gradebook=other_gradebook,
            course_enrollment=other_enrollment,
            grade_item=item["activity"],
            score=45,
        )
    recalculate_gradebook(other_gradebook, course_enrollments=[other_enrollment])

    client = APIClient()
    client.force_authenticate(user)
    response = client.get("/api/student/grades/")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["course_enrollment_id"] == course_enrollment.id
    assert response.data[0]["snapshot"]["final_status"] == GradeFinalStatus.APPROVED
    assert response.data[0]["snapshot"]["payload"]["learning_outcomes"]


@pytest.mark.django_db
def test_student_grade_view_hides_draft_gradebooks():
    gradebook = make_gradebook(code="S7T4C", grading_model=GradingModel.S1)
    gradebook.status = GradebookStatus.DRAFT
    gradebook.save()
    make_course_enrollment(code="S7T4C", course_section=gradebook.course_section)
    user = make_user("estudiante-s7t4c@example.edu", "USR-S7T4C", "Estudiante")
    enrollment = gradebook.course_section.course_enrollments.first()
    person = enrollment.enrollment.student.person
    person.user = user
    person.save()
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/student/grades/")

    assert response.status_code == 200
    assert response.data == []
