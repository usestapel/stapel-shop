# stapel-shop

Composite: catalog shop — categories + attributes + listings + reviews, with cross-domain glue projections.

> Likes/favourites are NOT included yet: `stapel-engagement` does not
> exist. They arrive as a MINOR bump of this composite once it does.

## Assemble (one line)

```bash
pip install stapel-tools
stapel-assemble myshop --libs shop
cd myshop && make test
```

That expands `shop` through the STAPEL_LIBS `requires`
closure and wires every member module into INSTALLED_APPS,
requirements.txt, urls.py and CONFIG.MD, then runs the verify gates.

## Manual wiring (no scaffold)

```python
# settings.py
from stapel_shop import preset

INSTALLED_APPS = [
    # ... django/stapel-core baseline (incl. stapel_core.django.projections)
    "stapel_categories",
    "stapel_listings",
    "stapel_reviews",
    "stapel_shop",
]
for _k, _v in preset.SETTINGS_DEFAULTS.items():
    globals().setdefault(_k, _v)

# urls.py
from django.urls import include, path

urlpatterns = [
    path("categories/", include("stapel_categories.urls")),
    path("listings/", include("stapel_listings.urls")),
    path("reviews/", include("stapel_reviews.urls")),
]
```

## Config checklist (fill these, in the generated project's CONFIG.MD too)

| Key | Note |
|-----|------|
| `STAPEL_REVIEWS["TARGET_TYPES"]` | prefilled by `stapel_shop.preset.SETTINGS_DEFAULTS` (targets `listing`); add `can_review`/`can_moderate` Functions to restrict |
| `STAPEL_LISTINGS["BASE_CURRENCY"]` | default `USD` — set your currency |
| `STAPEL_LISTINGS["DEFAULT_LISTING_TTL_DAYS"]` | default 30 |
| `STAPEL_REVIEWS["RATING_MIN"/"RATING_MAX"]` | defaults 1..5 |

## Glue (what this package actually contains)

- `stapel_shop.projections.ListingReviewSummaryProjection` — reviews→listings
  rating aggregate. Local mode (monolith): live reads through
  `reviews.aggregates_by_keys`. Remote mode: `ListingReviewSummary` table fed
  from `reviews.review.published/hidden` facts.
- Read it ONLY through
  `stapel_core.comm.projections.read("shop.listing_review_summary", keys=[...])`.
- Gap (stapel-reviews 0.1.0): `reviews.aggregates_by_keys` and
  `reviews.aggregates_export` are not shipped yet — reads/rebuild fail loudly
  until stapel-reviews adds them (declared here with the canonical names).
