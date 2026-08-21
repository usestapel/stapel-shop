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


def test_moderation_verdicts_are_not_crossed_between_members():
    """Two members subscribe to the SAME target-generic verdict topic.

    stapel-listings 0.4 made its ``moderation.completed`` consumer
    target-generic (it was `{listing_id}`-shaped before), so in this composite
    it shares one topic with reviews' consumer, and each decides "is this mine?"
    by its own ``MODERATION_TARGET_TYPE``. Those two names must stay disjoint —
    equal names would apply a review takedown to a listing with the same key.
    A composite that respells either one configures BOTH.
    """
    from stapel_core.comm.registry import action_registry
    from stapel_listings.conf import listings_settings
    from stapel_reviews.conf import reviews_settings

    assert len(action_registry.handlers("moderation.completed")) >= 2
    assert (
        listings_settings.MODERATION_TARGET_TYPE
        != reviews_settings.MODERATION_TARGET_TYPE
    )


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
    """The fact's ``aggregate`` maps onto the read-model columns, which carry
    the owner's names so both modes of ``read()`` answer one shape (see
    tests/test_projection_modes.py)."""
    from stapel_core.comm.projections import projection_registry

    proj = projection_registry.get("shop.listing_review_summary")

    class _Ev:
        payload = {
            "target_type": "listing",
            "target_key": "42",
            "aggregate": {"avg": 4.5, "count": 12},
        }

    assert proj.apply(_Ev()) == {"avg": 4.5, "count": 12}
