def pytest_configure(config):
    from django.conf import settings

    from stapel_core.testing import BASE_REST_FRAMEWORK

    if not settings.configured:
        settings.configure(
            SECRET_KEY="test-secret-key-not-for-production",
            INSTALLED_APPS=[
                "django.contrib.contenttypes",
                "django.contrib.auth",
                "django.contrib.sessions",
                "django.contrib.admin",
                "django.contrib.messages",
                "stapel_core.django.apps.CommonDjangoConfig",
                "stapel_core.django.users",
                "stapel_core.django.projections",
                "stapel_categories",
                "stapel_listings",
                "stapel_reviews",
                "stapel_shop",
            ],
            AUTH_USER_MODEL="users.User",
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:",
                }
            },
            DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
            USE_TZ=True,
            CACHES={
                "default": {
                    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                }
            },
            STAPEL_COMM={
                "OUTBOX_ENABLED": False,
                "ACTION_TRANSPORT": "inprocess",
            },
            # A harness that writes its own settings must still carry core's
            # exception handler, or DRF's default takes over and every refusal
            # no view code raises — 401/403 from authenticators and permission
            # classes, 404 from get_object_or_404, 405/406/415 from dispatch,
            # 429 from a throttle — answers a bare {"detail": ...} instead of
            # the fleet envelope (stapel_core.error_envelope.W001). Only this
            # one key: the rest of DRF's defaults stay as the suite had them.
            # Read off core's own test preset, never re-typed here.
            REST_FRAMEWORK={
                "EXCEPTION_HANDLER": BASE_REST_FRAMEWORK["EXCEPTION_HANDLER"],
            },
        )
        import django

        django.setup()
