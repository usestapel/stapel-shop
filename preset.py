"""Preset for the "shop" scenario — plain data, importable without
Django settings (projections-and-composition §3).

Scenario: a catalog shop (categories + typed attributes + listings + reviews).

A generated project (stapel-assemble … --libs shop) gets the
same wiring from the STAPEL_LIBS registry; this module is the single source
a hand-written settings.py/urls.py copies from instead.
"""

from .search_sources import LISTING_SOURCE

# Dotted app paths, in mount order. L1 libraries (stapel-attributes) are pip
# dependencies, NOT Django apps — deliberately absent here.
INSTALLED_APPS = [
    "stapel_categories",
    "stapel_listings",
    "stapel_reviews",
    "stapel_shop",
]

# (url_prefix, urlconf_module) — mount each one with
#   path(prefix, include(module))
# The composite itself mounts NO urls (http=False): it only carries glue.
# stapel-categories and stapel-listings contribute only ``v1/`` and expect the
# host to supply ``<mod>/api/``; a bare ``<mod>/`` serves ``/listings/v1/...``,
# which every client of the canon (``/listings/api/v1/...``) misses. The
# stapel-tools registry mounts the same prefixes (stapel-preset-gate).
URL_INCLUDES = [
    ("categories/api/", "stapel_categories.urls"),
    ("listings/api/", "stapel_listings.urls"),
    ("reviews/", "stapel_reviews.urls"),
]

# Scenario defaults for STAPEL_<MOD> settings dicts. Merge them into the
# project's settings, e.g.:
#   from stapel_shop import preset
#   STAPEL_REVIEWS = {**preset.SETTINGS_DEFAULTS.get("STAPEL_REVIEWS", {})}
SETTINGS_DEFAULTS = {
    "STAPEL_REVIEWS": {
        # reviews is target-generic and ships an EMPTY TARGET_TYPES registry;
        # the composite is the place that knows both sides, so the scenario
        # default targets the catalog's listings out of the box.
        "TARGET_TYPES": {
            "listing": {
                "moderation": "post",
                "one_per_author": True,
                "allow_response": True,
                # Host policy callbacks (comm Functions) are None by default:
                # any authenticated user may review. Register and name your
                # own "can_review"/"can_moderate" Functions to restrict.
            },
        },
    },
    # stapel-orders is a companion of this composite, not a member: a project
    # that installs it gets a cart over the catalog's listings with no glue.
    # Orders is purchasable-generic and ships an EMPTY registry; the listing
    # resolver is listings' own Function (stapel-listings >= 0.28).
    "STAPEL_ORDERS": {
        "PURCHASABLE_TYPES": {
            "listing": {"resolve": "listings.purchasables"},
        },
    },
    # stapel-search is a companion and ships BUILTIN_SOURCES = {}: it knows
    # nothing about listings. Without a source a host boots with
    # stapel_search.W001 and its search page is empty, so the composite
    # declares the one corpus it has.
    "STAPEL_SEARCH": {
        "SOURCES": {
            "listing": LISTING_SOURCE,
        },
    },
}
