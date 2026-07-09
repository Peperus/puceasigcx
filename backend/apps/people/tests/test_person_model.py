import pytest
from django.core.exceptions import ValidationError

from apps.people.models import Person
from apps.people.tests.factories import make_person, make_user


@pytest.mark.django_db
def test_person_identification_is_unique_when_present():
    make_person("ID-PEOPLE-001")

    with pytest.raises(ValidationError):
        make_person("ID-PEOPLE-001")


@pytest.mark.django_db
def test_person_identification_is_optional():
    Person.objects.create(first_name="Sin", last_name="Identificacion")
    Person.objects.create(first_name="Otra", last_name="Persona")

    assert Person.objects.filter(identification_number__isnull=True).count() == 2


@pytest.mark.django_db
def test_person_can_link_to_user():
    user = make_user("persona-vinculada@example.edu", "USR-PER-001")
    person = make_person("ID-PEOPLE-002", user=user)

    assert person.user == user
    assert user.person == person
