from django.conf import settings


def test_test_settings_use_in_memory_sqlite():
    database = settings.DATABASES["default"]

    assert settings.APP_ENVIRONMENT == "test"
    assert settings.DEBUG is False
    assert database["ENGINE"] == "django.db.backends.sqlite3"
    assert database["NAME"] == ":memory:" or str(database["NAME"]).startswith(
        "file:memorydb_"
    )
