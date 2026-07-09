from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from apps.academic_catalogs.tests.factories import make_career
from apps.people.models import Person
from apps.students.models import Student
from apps.teachers.models import Teacher


def make_user(email="usuario@example.edu", identification="USR-001", group_name=None):
    user = get_user_model().objects.create_user(
        email=email,
        password="Str0ng-pass-demo",
        names="Usuario",
        last_names="Sintetico",
        identification=identification,
    )
    if group_name:
        group, _created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
    return user


def make_person(
    identification_number="PER-001",
    first_name="Persona",
    last_name="Sintetica",
    user=None,
):
    return Person.objects.create(
        user=user,
        identification_number=identification_number,
        first_name=first_name,
        last_name=last_name,
        institutional_email=f"{identification_number.lower()}@example.edu",
        personal_email=f"{identification_number.lower()}@personal.example",
        phone="0990000000",
        birth_date=date(2000, 1, 1),
        address="Direccion sintetica",
    )


def make_student(person=None, career=None, student_code="EST-001"):
    if person is None:
        person = make_person(f"PER-{student_code}")
    if career is None:
        career = make_career(code=f"CAR-{student_code}")
    return Student.objects.create(
        person=person,
        student_code=student_code,
        career=career,
    )


def make_teacher(person=None, teacher_code="DOC-001", domains=None):
    if person is None:
        person = make_person(f"PER-{teacher_code}")
    teacher = Teacher.objects.create(
        person=person,
        teacher_code=teacher_code,
        academic_degree="Mgtr.",
        professional_title="Titulo sintetico",
        academic_profile="Perfil academico sintetico.",
    )
    if domains:
        teacher.domains.set(domains)
    return teacher
