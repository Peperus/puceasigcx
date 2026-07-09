import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APIClient

from apps.people.tests.factories import make_user
from apps.syllabus.models import SyllabusStatus
from apps.syllabus.services import approve_syllabus, finalize_syllabus, submit_syllabus
from apps.syllabus.tests.factories import make_complete_syllabus


@pytest.mark.django_db
@override_settings(SYLLABUS_SIGNED_FILE_MAX_BYTES=1024)
def test_authorized_user_uploads_signed_syllabus_pdf(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    secretary = make_user("secretaria-s5t7@example.edu", "USR-S5T7SEC", "Secretaria")
    syllabus = make_complete_syllabus("S5T7")
    finalize_syllabus(syllabus)
    submit_syllabus(syllabus)
    approve_syllabus(syllabus, user=secretary)
    client = APIClient()
    client.force_authenticate(secretary)
    uploaded_file = SimpleUploadedFile(
        "silabo firmado.pdf",
        b"%PDF-1.4\ncontenido sintetico\n%%EOF",
        content_type="application/pdf",
    )

    response = client.post(
        f"/api/syllabi/{syllabus.id}/upload-signed-file/",
        {"signed_file": uploaded_file},
        format="multipart",
    )

    assert response.status_code == 200
    syllabus.refresh_from_db()
    assert syllabus.status == SyllabusStatus.APPROVED
    assert syllabus.signed_file.name.endswith(".pdf")
    assert syllabus.signed_file_uploaded_by == secretary


@pytest.mark.django_db
def test_upload_rejects_non_pdf_file():
    secretary = make_user("secretaria-s5t7bad@example.edu", "USR-S5T7BAD", "Secretaria")
    syllabus = make_complete_syllabus("S5T7BAD")
    finalize_syllabus(syllabus)
    submit_syllabus(syllabus)
    approve_syllabus(syllabus, user=secretary)
    client = APIClient()
    client.force_authenticate(secretary)
    uploaded_file = SimpleUploadedFile(
        "silabo.txt",
        b"contenido sintetico",
        content_type="text/plain",
    )

    response = client.post(
        f"/api/syllabi/{syllabus.id}/upload-signed-file/",
        {"signed_file": uploaded_file},
        format="multipart",
    )

    assert response.status_code == 400
    assert "signed_file" in response.data
