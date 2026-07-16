from django.apps import AppConfig

# The composite's Projection declarations must be registered BEFORE
# stapel_core.django.projections' ready() runs wire_projections() /
# validate_registry() — and INSTALLED_APPS order puts the core projections
# app first in generated projects. Django imports every app's apps.py
# (populate phase 1) before calling any ready() (phase 3), so a module-level
# import here is what guarantees the ordering. projections.py is
# import-light: models are referenced as dotted strings, resolved lazily.
from . import projections  # noqa: F401  (Projection registration side effect)


class ShopConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stapel_shop"
    label = "shop"
    verbose_name = "Stapel Shop (composite)"
