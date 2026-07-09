import pytest
from django.core.exceptions import ValidationError

from apps.syllabus.models import BibliographyType, SyllabusBibliography, SyllabusStatus
from apps.syllabus.tests.factories import add_minimum_bibliography, make_syllabus


@pytest.mark.django_db
def test_teacher_can_manage_bibliography_while_syllabus_is_draft():
    syllabus = make_syllabus("S5T4")
    bibliography = add_minimum_bibliography(syllabus)

    bibliography.apa_reference = "Referencia sintetica actualizada."
    bibliography.save()
    bibliography.delete()

    assert not SyllabusBibliography.objects.filter(syllabus=syllabus).exists()


@pytest.mark.django_db
def test_bibliography_requires_apa_reference():
    syllabus = make_syllabus("S5T4REQ")

    with pytest.raises(ValidationError):
        SyllabusBibliography.objects.create(
            syllabus=syllabus,
            bibliography_type=BibliographyType.BASIC,
            apa_reference="",
        )


@pytest.mark.django_db
def test_bibliography_cannot_be_edited_when_syllabus_is_approved():
    syllabus = make_syllabus("S5T4LOCK")
    bibliography = add_minimum_bibliography(syllabus)
    syllabus.status = SyllabusStatus.APPROVED
    syllabus.save()

    bibliography.apa_reference = "Cambio no permitido."
    with pytest.raises(ValidationError):
        bibliography.save()
