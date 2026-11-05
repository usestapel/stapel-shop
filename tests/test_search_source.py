"""The `listing` search source this composite declares (SH1).

stapel-search ships ``BUILTIN_SOURCES = {}``: a host that installs it next to
this composite without a source boots with ``stapel_search.W001`` and its
search page lists nothing. The composite is the one place allowed to know
both sides, so it declares the corpus, and this file proves the declaration
end to end: a listing published through listings' own pipeline is pulled by
stapel-search over ``listings.search_documents`` and answered by
``search.query``.
"""
from decimal import Decimal

import pytest

from stapel_shop import preset


def test_preset_declares_the_listing_source():
    from stapel_shop import search_sources

    sources = preset.SETTINGS_DEFAULTS["STAPEL_SEARCH"]["SOURCES"]
    assert sources == {"listing": search_sources.LISTING_SOURCE}
    assert search_sources.LISTING_SOURCE == "stapel_shop.search_sources.listing_source"


def test_source_resolves_against_listings_functions():
    from stapel_core.comm import function_unreachable_reason
    from stapel_listings.models import INDEXED_STATUSES
    from stapel_search.registry import get_source

    spec = get_source("listing")
    assert spec.content_function == "listings.search_documents"
    assert spec.export_function == "listings.search_export"
    assert spec.key_fields[0] == "listing_id"
    assert spec.visible_statuses == frozenset(str(s) for s in INDEXED_STATUSES)
    assert not function_unreachable_reason(spec.content_function)
    assert not function_unreachable_reason(spec.export_function)


def test_host_boots_without_search_w001():
    from django.core import checks

    ids = {m.id for m in checks.run_checks()}
    assert "stapel_search.W001" not in ids
    assert "stapel_search.E004" not in ids


def test_invalidation_signals_are_subscribed():
    from stapel_core.comm.registry import action_registry

    for topic in ("listing.published", "listing.updated", "listing.removed"):
        assert action_registry.handlers(topic), topic


@pytest.mark.django_db
def test_published_listing_is_found_by_search_query(settings):
    from django.contrib.auth import get_user_model
    from stapel_categories.models import Category
    from stapel_core.comm import call
    from stapel_listings.models import Listing
    from stapel_listings.services.publish import publish_listing

    settings.STAPEL_LISTINGS = {"REQUIRE_IMAGE_ON_PUBLISH": False}
    owner = get_user_model().objects.create(username="seller", email="s@example.com")
    category = Category.objects.create(name="Lamps", slug="lamps")
    listing = Listing.objects.create(
        owner=owner,
        category_id=str(category.pk),
        language="en",
        currency="USD",
        title_draft="Brass desk lamp",
        description_draft="A heavy lamp with a green shade.",
        price_draft=Decimal("40.00"),
        lat_draft=Decimal("49.611600"),
        lon_draft=Decimal("6.131900"),
        geohash_draft="u0ubw2mtzz",
        location_label_draft="Luxembourg",
    )
    publish_listing(listing)
    listing.apply_moderation("approved")
    listing.refresh_from_db()

    body = call("search.query", {"type": "listing", "q": "lamp", "limit": 5})
    items = {item["key"]: item for item in body["items"]}
    assert str(listing.pk) in items
    card = items[str(listing.pk)]["card"]
    assert card["title"] == "Brass desk lamp"
    assert card["price"] == "40.00"
    assert card["currency"] == "USD"
