from .base import *  # noqa: F403

APP_ENVIRONMENT = env("APP_ENVIRONMENT", default="production")  # noqa: F405
DEBUG = False
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")  # noqa: F405

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
SECURE_HSTS_SECONDS = env.int(
    "DJANGO_SECURE_HSTS_SECONDS", default=31536000
)  # noqa: F405
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(  # noqa: F405
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=True,
)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)  # noqa: F405
SECURE_SSL_REDIRECT = env.bool(
    "DJANGO_SECURE_SSL_REDIRECT", default=False
)  # noqa: F405

# HTTPS redirection is expected at the reverse proxy in local Docker validation.
SILENCED_SYSTEM_CHECKS = ["security.W008"]
