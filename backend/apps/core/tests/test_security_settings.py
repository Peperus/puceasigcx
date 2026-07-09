from django.core.cache import cache
from django.test import override_settings
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView


class OnePerMinuteAnonThrottle(AnonRateThrottle):
    rate = "1/minute"


class ThrottledProbeView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [OnePerMinuteAnonThrottle]

    def get(self, request):
        return Response({"ok": True})


urlpatterns = [
    path("throttle-probe/", ThrottledProbeView.as_view(), name="throttle-probe"),
]


def test_rest_framework_security_defaults(settings):
    rest_framework = settings.REST_FRAMEWORK

    assert (
        "rest_framework_simplejwt.authentication.JWTAuthentication"
        in rest_framework["DEFAULT_AUTHENTICATION_CLASSES"]
    )
    assert (
        "rest_framework.throttling.AnonRateThrottle"
        in rest_framework["DEFAULT_THROTTLE_CLASSES"]
    )
    assert (
        "rest_framework.throttling.UserRateThrottle"
        in rest_framework["DEFAULT_THROTTLE_CLASSES"]
    )


@override_settings(ROOT_URLCONF=__name__)
def test_anon_rate_limiting_is_enforced():
    cache.clear()
    client = APIClient()

    first_response = client.get("/throttle-probe/")
    second_response = client.get("/throttle-probe/")

    assert first_response.status_code == 200
    assert second_response.status_code == 429
