"""Minimal composite checks: the package imports, the preset is coherent,
the Django app mounts, and the glue Projection declaration is valid.
"""
from stapel_shop import preset


def test_preset_is_coherent():
    # The composite's own app slot is present (glue must live in
    # INSTALLED_APPS — STAPEL_LIBS grabli 5.8) and prefixes are unique.
    assert "stapel_shop" in preset.INSTALLED_APPS
    prefixes = [p for p, _ in preset.URL_INCLUDES]
    assert len(prefixes) == len(set(prefixes))
    # The composite mounts no urls of its own (http=False — glue only).
    assert not any(m.startswith("stapel_shop") for _, m in preset.URL_INCLUDES)


def test_app_config_mounts():
    from django.apps import apps

    cfg = apps.get_app_config("shop")
    assert cfg.name == "stapel_shop"


def test_projection_declaration_registered_and_valid():
    """The glue projection is declared, resolves LOCAL when the owner module
    is co-installed (the composite's normal monolith shape), and passes the
    registry validation without a table check (local mode needs live_query,
    not model)."""
    from stapel_core.comm.projections import (
        projection_registry,
        resolve_mode,
        validate_registry,
    )

    proj = projection_registry.get("shop.listing_review_summary")
    assert proj.live_query == "reviews.aggregates_by_keys"
    assert proj.owner_label() == "reviews"
    assert resolve_mode(proj) == "local"  # stapel_reviews is installed here
    validate_registry()  # must not raise


def test_projection_not_wired_to_bus_in_local_mode():
    from stapel_core.comm.projections import wire_projections
    from stapel_core.comm.registry import action_registry

    wire_projections()
    assert action_registry.handlers("reviews.review.published") == []
    assert action_registry.handlers("reviews.review.hidden") == []


def test_apply_maps_aggregate_payload():
    from stapel_core.comm.projections import projection_registry

    proj = projection_registry.get("shop.listing_review_summary")

    class _Ev:
        payload = {
            "target_type": "listing",
            "target_key": "42",
            "aggregate": {"avg": 4.5, "count": 12},
        }

    assert proj.apply(_Ev()) == {"rating_avg": 4.5, "rating_count": 12}
