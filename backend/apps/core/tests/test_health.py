from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient


def test_health_endpoint_is_public():
    response = APIClient().get(reverse("health"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "puceasig"}


def test_version_endpoint_is_public():
    response = APIClient().get(reverse("version"))

    assert response.status_code == 200
    assert response.json() == {
        "service": "puceasig",
        "version": settings.APP_VERSION,
        "environment": "test",
    }
