# Changelog

## [0.2.0] - 2026-08-21

### Fixed — `ListingReviewSummaryProjection` did not actually work against the producer

stapel-reviews 0.2.0 shipped the two Functions this projection has named since
0.1.0 (`reviews.aggregates_by_keys`, `reviews.aggregates_export`), and the
first real contact proved three defects on this side. All three are now
covered by tests that run against the real producer, not a mock
(`tests/test_projection_modes.py`).

- **`from_snapshot()` was missing, so remote-mode `rebuild()` raised
  `TypeError`.** An export row is `{target_key, target_type, avg, count, seq}`;
  the inherited default drops only `target_key`/`seq` and handed the model
  `target_type` plus the owner's field names —
  `ListingReviewSummary() got unexpected keyword arguments: 'target_type',
  'avg', 'count'`. The projection now maps both of the owner's wire shapes (the
  fact's `aggregate` and an export row) through one mapper.
- **`read()` answered a different shape in each mode**, breaking stapel-core's
  "identical shape in both modes" contract: local mode returned the owner's
  `{avg, count}` verbatim (core has no hook to rename a `live_query` answer),
  remote mode returned the model's `{rating_avg, rating_count}`. Business code
  written in the monolith would have broken the day reviews was split out. The
  owner's names are now the contract shape on both sides.
- **The declaration documented an export that does not exist.** The docstring
  described both Functions as unshipped ("does not exist yet — remote-mode
  rebuild fails loudly") and never recorded the page shape, while
  `stapel_core.comm.projections._iter_snapshot` reads `resp["rows"]` and
  reviews serves `{rows, cursor, total}`. The docstring now records the real
  shapes: `{"keys": [...]} -> {key: {avg, count}}` for the `live_query`, and
  `{rows, cursor, total}` with a per-row `seq` in unix milliseconds — the same
  clock an Event timestamp uses, which is what lets a live fact arriving
  mid-rebuild outrank the snapshot row.

### Changed

- `ListingReviewSummary.rating_avg`/`rating_count` renamed to `avg`/`count`
  (migration `0002`, cutover-phase: add, carry the rows across, drop — one
  release, no window where both names are live). The read-model's columns are
  what remote-mode `read()` returns, so matching the owner's names is the only
  way to give both modes one shape.
- `stapel-reviews` floor raised to `>=0.2,<0.3` — the release that first
  carries the two Functions this module is declared against. Below it, local
  reads raise `FunctionNotRegistered` and rebuild has no source.

### Known gap (unchanged)

- reviews' facts and its export carry EVERY `target_type`, so remote mode also
  materialises non-listing targets: harmless extra rows keyed by their
  `target_key`, never joined to a listing. Payload filtering in the core
  Projection primitive (or per-type topics in reviews) is the clean fix.

## [0.1.5] - 2026-08-02

### Fixed - `tests/test_contract.py` (added in 0.1.4) needs `stapel-tools` on the release track too

`ci.yml`'s test job already installs `"stapel-tools>=0.9.1,<1"` explicitly
(via its own migration-lint fix), but `publish.yml`'s test job did not —
`stapel_tools.llms_txt` (imported by `tests/test_contract.py`) failed to
collect there with `ModuleNotFoundError`, and the v0.1.4 tag's publish run
never got past `test` (no wheel was built, nothing was published — this
module has never reached PyPI regardless, see below). `publish.yml` now
installs `"stapel-tools>=0.9.1,<1"` in "Install test dependencies" too.

## [0.1.4] - 2026-08-02

Packaging/CI only, no runtime change.

### Changed
- Canonical `ci.yml` with coverage, `codecov.yml`, Python 3.14 trove
  classifier, badge canon (this module is not yet on PyPI, so only the
  license + CI-status badges apply — no pypi/downloads/coverage/python
  badges, and the README honestly says install-from-source).
- Contract documents (`docs/capabilities.json`, `docs/flows.json`,
  `docs/errors.json`, `CONFIG.MD`) ship inside the wheel via `package-data` (#184).
- New Makefile (the module had none) with `contract`/`contract-check`
  targets plus `tests/test_contract.py`, wiring `docs/llms.txt` — the
  fifth contract artifact (badge-canon §3) — from the hand-authored
  `docs/capabilities.json`; now packaged into the wheel.
- `docs/capabilities.json`'s hand-maintained `version` field brought back
  in line with `pyproject.toml` (it had drifted to 0.1.2 while the package
  moved to 0.1.3).

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
