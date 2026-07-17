# Changelog

## [0.1.2] - 2026-07-17

Fleet follow-up to stapel-core 0.12.0 (legacy shim sweep). Also re-pins
member ceilings that had gone stale since 0.1.1: `stapel-categories` had
since had a breaking bump to 0.5.0 and `stapel-attributes` to 0.4.0,
both outside this composite's old `<0.5`/`<0.4` ceilings — publish would
have hit ResolutionImpossible even with the core fix. Suite green.

### Changed
- `stapel-core` ceiling `<0.12` → `<0.13`.
- `stapel-categories` ceiling `<0.5` → `<0.6`.
- `stapel-attributes` ceiling `<0.4` → `<0.5`.

## [0.1.1] - 2026-07-17

### Changed
- `stapel-core` ceiling raised `>=0.10,<0.11` → `>=0.10,<0.12` (core 0.11
  fleet re-pin: default bus, nav, config-checks, error params/language —
  additive for modules). Member-module pins (categories, attributes,
  listings, reviews) already satisfied by their own 0.11-fleet patch
  releases. Suite green as-is.

## [0.1.0] - 2026-07-16

### Added

- Initial composite (projections-and-composition §3): pyproject pins over
  the member modules, `preset` (INSTALLED_APPS/urls/STAPEL_* defaults),
  glue projection `shop.listing_review_summary` (reviews → listings), AppConfig app slot, minimal tests.

### Known gaps

- Likes/favourites wait for `stapel-engagement` (minor bump when it exists).
- `reviews.aggregates_by_keys` / `reviews.aggregates_export` must land in stapel-reviews for local reads / remote rebuild of `shop.listing_review_summary`.
