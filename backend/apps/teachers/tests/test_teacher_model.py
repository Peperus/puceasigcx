import pytest
from django.db import IntegrityError

from apps.academic_catalogs.tests.factories import make_domain
from apps.people.tests.factories import make_person, make_teacher
from apps.teachers.models import Teacher


@pytest.mark.django_db
def test_person_can_have_teacher_profile_with_syllabus_data():
    domain = make_domain("DOM-TEACH-001")
    person = make_person("ID-TEACHER-001")

    teacher = make_teacher(person=person, teacher_code="DOC-MODEL-001")
    teacher.domains.add(domain)

    assert person.teacher_profile == teacher
    assert teacher.academic_profile
    assert list(teacher.domains.all()) == [domain]


@pytest.mark.django_db
def test_teacher_code_is_unique():
    first_teacher = make_teacher(teacher_code="DOC-UNIQUE-001")
    second_person = make_person("PER-DOC-UNIQUE-002")

    with pytest.raises(IntegrityError):
        Teacher.objects.create(
            person=second_person,
            teacher_code=first_teacher.teacher_code,
        )
