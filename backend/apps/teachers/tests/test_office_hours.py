from datetime import time

import pytest
from django.core.exceptions import ValidationError

from apps.people.tests.factories import make_teacher
from apps.teachers.models import TeacherOfficeHour


@pytest.mark.django_db
def test_teacher_can_have_multiple_office_hours():
    teacher = make_teacher(teacher_code="DOC-OH-001")

    TeacherOfficeHour.objects.create(
        teacher=teacher,
        modality="presencial",
        day_of_week=1,
        start_time=time(9, 0),
        end_time=time(10, 0),
        location_or_link="Aula sintetica",
    )
    TeacherOfficeHour.objects.create(
        teacher=teacher,
        modality="virtual",
        day_of_week=3,
        start_time=time(15, 0),
        end_time=time(16, 0),
        location_or_link="https://example.edu/tutoria",
    )

    assert teacher.office_hours.count() == 2


@pytest.mark.django_db
def test_invalid_office_hour_range_is_rejected():
    teacher = make_teacher(teacher_code="DOC-OH-002")

    office_hour = TeacherOfficeHour(
        teacher=teacher,
        modality="presencial",
        day_of_week=1,
        start_time=time(10, 0),
        end_time=time(10, 0),
        location_or_link="Aula sintetica",
    )

    with pytest.raises(ValidationError):
        office_hour.full_clean()
