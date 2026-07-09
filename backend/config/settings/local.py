from .base import *  # noqa: F403

APP_ENVIRONMENT = env("APP_ENVIRONMENT", default="local")  # noqa: F405
DEBUG = env.bool("DJANGO_DEBUG", default=True)  # noqa: F405
ALLOWED_HOSTS = env.list(  # noqa: F405
    "DJANGO_ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1", "0.0.0.0"],
)

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
)
