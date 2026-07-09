import pytest
from django.core.exceptions import ValidationError

from apps.academic_catalogs.tests.factories import make_career, make_plan
from apps.people.tests.factories import make_person, make_student
from apps.students.models import Student


@pytest.mark.django_db
def test_person_can_have_student_profile():
    person = make_person("ID-STUDENT-001")
    student = make_student(person=person, student_code="EST-MODEL-001")

    assert student.person == person
    assert person.student_profile == student


@pytest.mark.django_db
def test_student_code_is_unique():
    first_student = make_student(student_code="EST-UNIQUE-001")
    second_person = make_person("PER-EST-UNIQUE-002")

    with pytest.raises(ValidationError):
        Student.objects.create(
            person=second_person,
            student_code=first_student.student_code,
            career=first_student.career,
        )


@pytest.mark.django_db
def test_student_study_plan_must_match_career():
    career = make_career("CAR-ST-001")
    other_career = make_career("CAR-ST-002")
    other_plan = make_plan(other_career, "PLAN-ST-002")

    student = make_student(career=career, student_code="EST-PLAN-001")
    student.study_plan = other_plan

    with pytest.raises(ValidationError):
        student.full_clean()
