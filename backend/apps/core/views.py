from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = []

    def get(self, request):
        return Response({"status": "ok", "service": settings.APP_NAME})


class VersionView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = []

    def get(self, request):
        return Response(
            {
                "service": settings.APP_NAME,
                "version": settings.APP_VERSION,
                "environment": settings.APP_ENVIRONMENT,
            }
        )
