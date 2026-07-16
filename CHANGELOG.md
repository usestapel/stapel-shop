# Changelog

## [0.1.0] - 2026-07-16

### Added

- Initial composite (projections-and-composition §3): pyproject pins over
  the member modules, `preset` (INSTALLED_APPS/urls/STAPEL_* defaults),
  glue projection `shop.listing_review_summary` (reviews → listings), AppConfig app slot, minimal tests.

### Known gaps

- Likes/favourites wait for `stapel-engagement` (minor bump when it exists).
- `reviews.aggregates_by_keys` / `reviews.aggregates_export` must land in stapel-reviews for local reads / remote rebuild of `shop.listing_review_summary`.
