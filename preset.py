"""Preset for the "shop" scenario — plain data, importable without
Django settings (projections-and-composition §3).

Scenario: a catalog shop (categories + typed attributes + listings + reviews).

A generated project (stapel-assemble … --libs shop) gets the
same wiring from the STAPEL_LIBS registry; this module is the single source
a hand-written settings.py/urls.py copies from instead.
"""

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
URL_INCLUDES = [
    ("categories/", "stapel_categories.urls"),
    ("listings/", "stapel_listings.urls"),
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
}
