import pytest
from rest_framework.test import APIClient

from apps.grading.models import GradingModel
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
def test_permission_student_cannot_see_other_student_grades():
    own_gradebook = make_gradebook(code="S8PERM1", grading_model=GradingModel.S1)
    other_gradebook = make_gradebook(code="S8PERM2", grading_model=GradingModel.S1)
    open_gradebook(own_gradebook)
    open_gradebook(other_gradebook)
    own_items = add_s1_s2_structure(own_gradebook)
    other_items = add_s1_s2_structure(other_gradebook)
    own_enrollment = make_course_enrollment(
        code="S8PERM1",
        course_section=own_gradebook.course_section,
    )
    other_enrollment = make_course_enrollment(
        code="S8PERM2",
        course_section=other_gradebook.course_section,
    )
    user = make_user("estudiante-s8perm@example.edu", "USR-S8PERM", "Estudiante")
    own_enrollment.enrollment.student.person.user = user
    own_enrollment.enrollment.student.person.save()
    for item in own_items:
        save_grade_record(
            gradebook=own_gradebook,
            course_enrollment=own_enrollment,
            grade_item=item["activity"],
            score=40,
        )
    for item in other_items:
        save_grade_record(
            gradebook=other_gradebook,
            course_enrollment=other_enrollment,
            grade_item=item["activity"],
            score=45,
        )
    recalculate_gradebook(own_gradebook, course_enrollments=[own_enrollment])
    recalculate_gradebook(other_gradebook, course_enrollments=[other_enrollment])
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/student/grades/")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["course_enrollment_id"] == own_enrollment.id


@pytest.mark.django_db
def test_permission_teacher_cannot_edit_unassigned_gradebook():
    assigned = make_gradebook(code="S8PERM3", grading_model=GradingModel.S1)
    unassigned = make_gradebook(code="S8PERM4", grading_model=GradingModel.S1)
    open_gradebook(unassigned)
    items = add_s1_s2_structure(unassigned)
    enrollment = make_course_enrollment(
        code="S8PERM4",
        course_section=unassigned.course_section,
    )
    user = make_user("docente-s8perm@example.edu", "USR-S8PERMT", "Docente")
    assigned.syllabus.lead_teacher.person.user = user
    assigned.syllabus.lead_teacher.person.save()
    client = APIClient()
    client.force_authenticate(user)

    response = client.post(
        f"/api/grading/teacher/gradebooks/{unassigned.id}/record/",
        {
            "course_enrollment": enrollment.id,
            "grade_item": items[0]["activity"].id,
            "score": "40",
        },
        format="json",
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_permission_student_cannot_access_mvp_academic_reports():
    user = make_user("estudiante-s8perm2@example.edu", "USR-S8PERM2", "Estudiante")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/reports/mvp/grades/")

    assert response.status_code == 403
