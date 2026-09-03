# Changelog

## [0.2.27] — 2026-09-03

Patch. Caps only: `stapel-categories` admits 0.17, `stapel-listings` admits
0.18/0.19.

stapel-categories 0.17.0 lets a per-category feature OVERRIDE carry its own
display `name` — both halves of the fixture round trip used to drop it, so
every override rendered the ROOT's label — and turns a malformed category id
into the `LookupError` its docstrings promise instead of a 500.

stapel-listings 0.18/0.19 land in one release: `listings_reproject_features`
can BUILD a missing projection (it was keyed on its own output, so a listing
carrying a draft and no projection was never even examined, and a live fleet
had 12 published rows showing an empty characteristics table), and
`Listing.category_id` gained a model-field validator so it can hold an id and
not a search path.

None of it touches a surface this module reads: shop runs no catalogue load,
holds no sidecar, reads the tree through the comm Functions, and consumes
listings through `listings.status` and the card projection. The suite is green
against both with no edit — so this is a cap-only patch, and holding it is what
would keep a fleet from installing the fix for a defect it is already
suffering.

## [0.2.26] — 2026-09-03

Patch. Cap only: `stapel-attributes` admits 0.9.

stapel-attributes 0.9.0 changes one rule semantic — a VALUE predicate (`in` /
`not_in`) no longer matches a controller that reads EMPTY, so a
`require when X not_in […]` rule stops firing before anyone has answered `X`.
Two UX walkers had hit that wall on an imported catalogue: a field starred and
refusing "Next" while its own help line said it was needed only *if* another
field said so, with that field untouched.

The cap moves so a fleet can install one attributes version. `tests/
test_pin_coherence.py` is the only file in this module that reads the line —
it checks the declared range against what is actually installed — and it is
the test that went red the moment 0.9.0 landed in the venv. Green again, with
no other edit.

## [0.2.25] — 2026-09-03

### Changed

- `stapel-categories` cap `<0.16` -> `<0.17`. Range only: 0.16.0 changes the
  public HTTP reads (retired dead-end rows leave the catalogue; a service or
  staff sync principal still gets the full set) and touches none of the comm
  Functions this module reads the tree through.

## [0.2.24] — 2026-09-03

### Fixed

- Re-cut of 0.2.23, whose tag was pushed before the regenerated
  version-stamped artifacts and failed its own drift gate on the way to
  PyPI. Same range change, nothing else. Pin 0.2.24.

## [0.2.23] — 2026-09-03 (never published)

### Changed

- `stapel-listings` cap `<0.16` -> `<0.18`. Range only: 0.16 requires a
  location to publish and derives the published `location_label` from the
  pin, 0.17 adds the batched engagement overlay, and none of the three
  touches a surface this module reads. Held where it was, the cap pinned
  every fleet that installs shop to a listings that publishes placeless rows.

## [0.2.22] — 2026-09-03

Patch. One cap — no code, no model, no migration, no payload.

- `stapel-categories<0.15` -> `<0.16`

**stapel-categories 0.15.0** makes `active` stand-owned curation: a
catalogue re-import writes it only on create, so it can no longer resurrect
a category an operator retired in the admin — the same failure the
presentation keys were pulled out for in 0.13.0, one field over. It also
adds the resurrection half of the `catalog_health` gate (an active category
under an inactive parent: reachable by search or a saved link while the path
to it is closed). Breaking for a `.sync-state.json` sidecar
(`STATE_VERSION` 3 -> 4) and for anyone who expected a fixture's `active` to
win on update; this module runs no catalogue load and holds no sidecar.

## [0.2.21] — 2026-09-02

Patch. One cap — no code, no model, no migration, no payload.

- `stapel-listings<0.15` -> `<0.16`

**stapel-listings 0.15.0** is breaking twice over, and neither break reaches
this module: `price` is nullable (an unstated price is NULL, never a public
"0 ₽" on a card), and the index-boundary detector moved into
`Listing.save()`, so a status write that skipped the state machine can no
longer leave a de-listed listing in a search index. A reader of
`Listing.price` has to look at both; this module holds one review-summary
projection keyed by listing id and reads no listing field at all. So the cap
was again the only wall — and a fleet held behind it keeps serving ghost
cards and free phones.

## [0.2.20] — 2026-09-02

Patch. Caps only — no code, no model, no migration, no payload.

- `stapel-categories<0.14` -> `<0.15`
- `stapel-listings<0.14` -> `<0.15`

This module reads neither of the things behind them; the cap is again the
only wall in front of a fleet that does. **stapel-categories 0.14.0** adds
the `categories.children` comm Function — the rung-by-rung tree read an LLM
walks a category guess with, the way a person walks the cascade.
**stapel-listings 0.14.0** claims CDN media references for a listing's
photos, so stapel-cdn's orphan sweeper can tell a live photo from an
abandoned upload.

## [0.2.19] — 2026-09-02

Dependency-range patch, no code. `stapel-categories<0.13` -> `<0.14`: the cap
sat in front of a member of the classified composite the day categories
0.13.0 shipped (the release that takes source-catalogue provenance off the
public read surface), turning a fleet's security bump into
ResolutionImpossible. Verified against 0.13.0: this package's suite passes
unmodified — it consumes the tree and the feature schema, neither of which
moved.

## [0.2.18] — 2026-09-02

Patch. Caps only — no code, no model, no migration, no payload.

- `stapel-categories<0.12` -> `<0.13`
- `stapel-listings<0.13` -> `<0.14`

This module reads neither of the things behind them. The cap is, again, the
only thing standing in front of a fleet that does — the failure shape this
block has now recorded seven times.

**stapel-categories 0.12.0** adds the two public tree reads a storefront
walks a catalogue with: `roots` (top-level categories without pulling the
whole table) and `by-slug/<slug>` (the storefront's own URL vocabulary
resolved server-side). Until they existed, a client that wanted either had
one way to ask — list everything and filter locally, measured on a live stand
as a 15-page, 614 KB walk behind a cold catalogue page.

**stapel-listings 0.13.0** makes `listings_reproject_features` repair a
listing field by field instead of skipping the whole row over one attribute
that no longer validates. Held at `<0.13`, this cap is what keeps 12 measured
listings on a stale projection, printing storage slugs where display copy
belongs.

## [0.2.17] — 2026-09-02

Patch. Caps only — no code, no model, no migration, no payload.

- `stapel-attributes<0.8` -> `<0.9`
- `stapel-categories<0.11` -> `<0.12`
- `stapel-listings<0.12` -> `<0.13`

The three move TOGETHER because each alone is a no-change: the axis is
declared in one, set in the second and enforced in the third, and any two of
them without the last resolves to a fleet that still publishes the value.

What they are in front of: an anonymous GET of a listing on a live classified
stand answered with the car's **VIN**, and the same string sat in
`features_search`, where `?f.vin=<value>` made the search index an oracle —
it would confirm that this exact advert is that exact vehicle. A VIN and an
IMEI identify a *specific physical unit* rather than describing it, so
publishing one lets a stranger act as its owner. stapel-attributes 0.8.0 adds
`FeatureDef.visibility` and stamps it onto every stored value (so a card, a
search document and a bus payload can tell without a schema in hand),
stapel-categories 0.11.0 adds the column the catalogue sets it in, and
stapel-listings 0.12.0 stops handing the value to a reader without the
entitlement.

This module reads none of it — `grep -rn stapel_attributes *.py` is still
empty and these three appear only as dotted paths in `preset.py` — which is
exactly why the caps are the whole coupling and why a stale one is invisible
until pip answers ResolutionImpossible instead of warning. The floors do not
move, for the reason this file has now given several times: a floor on a
package this composite does not touch is a statement about what it needs,
which is nothing.

## [0.2.16] — 2026-09-02

Patch. Cap only — no code, no model, no migration, no payload.

`stapel-categories<0.10` -> `<0.11`. 0.10.0 grades a `categories.suggest`
match four ways where it graded it two, so the caller that ranks a type-ahead
can put an exact catalogue name above a fragment buried inside an unrelated
word. This module calls no part of that Function; the cap was simply the wall
in front of it, exactly as it was in 0.2.14 — held here, pip answers
ResolutionImpossible for anything installing this module beside categories
0.10.

## [0.2.15] — 2026-09-01

Patch. One dependency comment — no code, dependency range or API change.

The comment explaining why the `stapel-attributes` cap moved named the
external marketplace whose catalogue was imported. It now says what the
argument rests on: an imported external catalogue, 2 468 of whose fields are
composites.

## [0.2.14] — 2026-08-31

### Changed — the cap was the wall in front of a sibling's release

0.2.13 carried the same cap bump and never published: the version moved in
`pyproject.toml` and `docs/capabilities.json` was left describing 0.2.12, so
the drift gate refused the release — correctly, since a contract artifact
that lags the package it describes is exactly what that gate exists to catch.

Patch (pre-1.0 semver: minor = breaking, patch = compatible). No model,
migration, view or code change: this release admits a sibling and does
nothing else.

- **`stapel-categories<0.9` → `<0.10`.** 0.9.0 adds the `categories.suggest`
  comm Function — category NAMES matched for a type-ahead, answered with their
  full ancestry — which is what lets a classified's search box offer
  «Одежда › Мужская одежда › Шорты» instead of three identical strings.
  Nothing of it is consumed here: it is a new Function on a surface this
  module does not call, and no model, migration or payload moved. Held at
  `<0.9`, this line is the wall rather than the guard — pip answers
  `ResolutionImpossible` for anything installing this module beside the
  release, and a fleet that needs both has no solution at all.

## [0.2.12] — 2026-08-31

### Changed

- **`stapel-listings<0.11` → `<0.12`.** 0.2.11 widened the `stapel-attributes`
  cap to admit 0.7.0 — the release that snapshots option copy into a stored
  `select` DAO — and that widening did nothing on its own. stapel-listings
  0.11.0 declares `stapel-attributes>=0.7,<0.8`, so with listings held under
  0.11 the two lines have no common solution and pip answers by resolving
  attributes back to 0.6.2. Not an error, not a warning: a fleet that believed
  it had the fix, and cards that keep printing `b-u`. The cap was found by a
  pin-coherence gate one repository over, which is where this class of defect
  is always found and never by the repository that caused it.

  0.11.0 also carries `listings_reproject_features`, the command that
  re-derives the four projections from the stored draft and the current
  category schema. A write-time snapshot has no other way to become true
  again, and every listing published before attributes 0.7.0 is a stale one.

  Nothing in this package imports `stapel_listings`; the range is the whole
  coupling, so the floor stays at 0.4.

## [0.2.11] — 2026-08-31

### Changed

- **`stapel-attributes<0.7` → `<0.8`.** 0.7.0 snapshots the chosen options'
  `label` copy into `SelectDao.labels`, positionally aligned with `value`, so a
  stored `select` renders as copy rather than as its storage slug without the
  reader fetching the category config. A live classified deployment was
  printing slugs at people on listing cards, detail pages and facet chips. The
  four projections this composite declares are precisely those readers, so
  capping under 0.7 caps a fleet under the only version that spells this
  composite's own output correctly — and pip does not warn about it, it answers
  `ResolutionImpossible` beside stapel-categories 0.8.4. The seventh cap in
  this composite's history to be the wall rather than the guard.

Nothing here reads the new field — nothing here reads attributes at all — so
the **floor stays at `>=0.3`**, and that is a measurement rather than an
inheritance: `grep -rn stapel_attributes *.py` in this repository is empty. The
package appears only as a dotted path in `preset.py`'s `INSTALLED_APPS`. There
is no import to break, no DAO built here and no `labels` read here, so the
range is the whole coupling and the floor states what this composite itself
needs, which is nothing. A host that wants the label snapshot declares its own
`>=0.7` and this line gets out of the way.

### Known: this composite is no longer the wall, but the wave is not resolvable yet

Every published `stapel-listings`, 0.10.3 included, declares
`stapel-attributes>=0.6,<0.7`. Against the workspace with attributes 0.7.0
installed, the pin gate is down to one failure and it names that member rather
than a cap here:

    stapel-listings 0.10.2 requires 'stapel-attributes<0.7,>=0.6',
    but stapel-attributes 0.7.0 is installed

Which is the gate working as its own docstring describes — "unless a git-main
member has outgrown a cap". Resolved from these specifiers as pip actually
does, listings holds the fleet at attributes 0.6.2 and the suite is
**21 passed**: that is the combination this release publishes, and it is green.
Reaching 0.7.0 needs listings to move its own cap, which is filed for that
repository rather than worked around here — widening a cap this composite does
not own would be a lie in metadata, the exact defect every entry above records.

**And the next cap here is already visible.** stapel-listings' working tree is
mid-release to **0.11.0** with `stapel-attributes>=0.7,<0.8` — the moment that
publishes, this composite's `stapel-listings>=0.4,<0.11` becomes the wall in
its turn and needs 0.2.12. It is deliberately NOT widened in this release:
0.11.0 is unpublished and untested, and a composite whose entire product is a
combination known to work cannot admit a version no suite has ever run against.
A cap here states the range this package was built against; pre-widening it
would make the claim false in the same breath that fixes the other one.

### Changed

- **`stapel-reviews<0.5` → `<0.6`.** stapel-reviews 0.5.0 is where the module
  subscribes `user.merged` and re-parents an author's reviews onto the
  surviving account. `stapel_core.lifecycle.E001` makes that an ERROR rather
  than a nicety: an app that handles `user.deleted` and says nothing about
  `user.merged` strands the merged account's rows behind an id that can no
  longer sign in, and `manage.py check` reports the silence. Every host that
  mounts this composite therefore has to be able to reach reviews 0.5, and
  under the old cap it could not: pip answers `ResolutionImpossible` for
  anything declaring `stapel-reviews>=0.5` beside this line — which is what
  held stapel-classified 0.5.1, 0.5.2 and 0.5.3 off PyPI, three publish runs
  in a row. The sixth cap in this composite's history to be the wall rather
  than the guard.

Nothing here reads reviews' new consumer, so the floor stays at `>=0.2` — the
range is the whole coupling. 21 passed.

## [0.2.9] — 2026-08-31

### Changed

- **`stapel-attributes<0.6` → `<0.7`.** 0.6.0 adds the composite `group` kind
  and both members this composite pins — stapel-categories 0.8.3 and
  stapel-listings 0.10.2 — require it. Held at `<0.6` this line has no
  solution: pip answers `ResolutionImpossible` for anything installing this
  composite next to them, which is the same trap the `stapel-categories` line
  above already records twice. Nothing here reads the new type; the range is
  the whole coupling.

## [0.2.8] — 2026-08-31

### The categories cap excluded the release that stops losing rows on a re-sync

`stapel-categories<0.8` is the fifth cap in this composite's history to be the
wall rather than the guard. **0.8.0 stops keying a catalog re-import on the
slug**: an imported category's slug is derived from the source catalogue's node
path, so when the source renames a node the slug moves and the node id does
not, and a slug-keyed re-import read that as "one category disappeared, an
unrelated one appeared" — soft-deleting the row that holds the listings and
creating a duplicate beside it. Matching is now `(external_source,
external_id)` first, the slug only as a fallback. A composite whose subject is
an imported marketplace catalog cannot cap a fleet under that.

**0.8.1** is the other half and is a floor for anyone importing at scale rather
than a nicety: django-treenode rebuilt its denormalized tree columns from a
`post_save` receiver, once per row written, and `load_catalog` writes every
record through `save()` by design — so the cost was worse than quadratic. A
2901-leaf import (3444 categories, 14 409 feature rows) did not finish; 0.8.1
rebuilds once per load and it takes 185 s.

`>=0.4,<0.9`, so the range still admits everything it did before. Nothing in
this composite reads a removed field: 0.8.0 is expand-only (one `AddField`,
one `AddIndex`, migration `0004`) and 0.8.1 changes no surface at all.

## [0.2.7] — 2026-08-30

### The attributes cap had no solution at all

`stapel-attributes>=0.3,<0.5` was not merely stale after the attributes-v2
wave — it was self-contradictory next to its own sibling. **stapel-categories
0.7.0 requires `stapel-attributes>=0.5,<1.0`**, so no version of attributes
satisfied both this composite and a member of it. pip answers
`ResolutionImpossible`, not a warning, and `stapel-classified` 0.5.0 — which
pins categories 0.7.0, attributes 0.5.1 and listings 0.10.0 while keeping
`stapel-shop>=0.2.6,<0.3` — could not be installed at all.

Now `stapel-categories>=0.4,<0.8`, `stapel-attributes>=0.3,<0.6`,
`stapel-listings>=0.4,<0.11`. Floors are unchanged: nothing here grew a
dependency on the new surface.

The wave itself (attributes 0.5.1 / categories 0.7.0 / listings 0.10.0) gives
`FeatureDef` its `rules`, `description`, `example`, `default`, `hints` and
`group`; makes requiredness the rule state rather than static `mandatory`;
drops a rule-hidden feature from the DAO instead of merely leaving it
unvalidated; and adds `ref_select` / `ref_hierarchical_select`, whose values
travel as vocabulary **codes** plus a `labels` snapshot.

None of that reaches this composite's own surface, and that is a fact about
the code, not an assumption: this package reads no feature config and no
feature DAO anywhere. `preset.py` is plain data (`INSTALLED_APPS`,
`URL_INCLUDES`, reviews' `TARGET_TYPES`); the single glue projection is
reviews → listings and touches `avg`/`count` only. There is no type-slug
list to widen, no `mandatory` read, and no `select` value formatted without
its `labels`. Verified against the three released siblings: full suite green
(21 passed).

One composition note for a project that uses the new ref types: a `ref_*`
config is loud without a registered vocabulary resolver
(`STAPEL_ATTRIBUTES["VOCABULARY_RESOLVER"]`, or
`register_vocabulary_resolver` from an `AppConfig.ready()`). The resolver
implementation ships outside stapel-attributes, so wiring one is a project
decision; adding a member to this composite would be a minor bump, not this
one.

### Added — a pin-coherence gate (`tests/test_pin_coherence.py`, 2 tests)

Every release since 0.2.4 has fixed the same defect: a cap here excluded a
member version the fleet had to install. Nothing in this repo could catch it,
because no code here reads a member's surface — the contradiction lives
entirely in metadata. So the gate reads metadata: this package's specifiers
must admit the member versions the suite actually ran against, and every
member's own requirement on a fellow stapel distribution must be satisfied by
that same set. Run against 0.2.6's pins with the wave installed, it named all
three stale caps by version and specifier before they were widened.

## [0.2.6] — 2026-08-30

### The caps made the guest wall unbuildable

`stapel-listings>=0.4,<0.9` and `stapel-reviews>=0.2,<0.4` held every fleet
below listings **0.9.0** and reviews **0.4.0** — the two releases that
introduce `ALLOW_ANONYMOUS_WRITES`, the server-side decision on whether a
guest may write.

A client fleet running the classified composite already writes
`STAPEL_LISTINGS["ALLOW_ANONYMOUS_WRITES"] = False` and
`STAPEL_REVIEWS["ALLOW_ANONYMOUS_WRITES"] = False` in its settings. On the
installed versions the key does not exist, so nothing reads it: a guest is a
real authenticated user, satisfies `IsAuthenticated`, and can create and
publish a listing and leave a review. The setting looks like a wall in the
config and is a comment in practice. Confirmed against the running stand
before this was raised.

Neither cap could be widened from the fleet side — pip answers
ResolutionImpossible rather than warning, and this composite was one of the
two walls (the other is `stapel-classified`, which lifts its own in 0.4.2).
Now `stapel-listings>=0.4,<0.10` and `stapel-reviews>=0.2,<0.5`.

Nothing in the composite changes shape. Both new releases are additive on the
surfaces this package touches: it mounts `stapel_listings.urls` and reads
reviews' facts through `ListingReviewSummaryProjection`; the preset is plain
data. Neither the new setting nor listings 0.9.0's guest-favourite merge on
sign-in reaches a permission class or a declared serializer type here.
Verified against listings 0.9.0 + reviews 0.4.0: full suite green (19 passed).

## [0.2.5] — 2026-08-28

### The listings cap pinned every fleet to a leaking version

`stapel-listings>=0.4,<0.8` kept deployments below 0.8.0, which closes a live
anonymous enumeration oracle: the status probe returned `owner_id` and
`moderation_status` for any listing id, over sequential ids, including other
people's drafts, rejected and soft-deleted rows. Confirmed against a running
stand before this was raised.

pip refuses the resolution outright rather than warning, so the cap did not
merely discourage the upgrade — it made it impossible while this composite was
installed. Now `<0.9`.

The only change 0.8.0 makes to this composite's surface is that a stranger
receives one `is_deleted` boolean from the status probe where it used to
receive six fields. Nothing here reads the removed ones.

## [0.2.4] - 2026-08-24

### Changed — pins widen to admit `stapel-listings` 0.7

`stapel-listings>=0.4,<0.7` → `<0.8`. This is the release that lets a fleet
install **listings 0.7.1** — geohash stamping on `Listing.save()` plus the
`listings_backfill_geohash` management command (the fix for stapel-search
0.2.2's geohash prefilter, which had nothing to prefilter against while
every listing carried `geohash=""`). 0.7.0's only change was an additive
route (`GET my/listings/`); this composite touches neither that route nor
any listings internal beyond mounting `stapel_listings.urls`, so nothing
here changes shape. Verified in a clean venv on released listings 0.7.1:
full suite green (19 passed), `pip check` clean.

## [0.2.3] - 2026-08-22

### Changed — pins widen to admit `stapel-listings` 0.6 and `stapel-reviews` 0.3

`stapel-listings>=0.4,<0.6` → `<0.7`; `stapel-reviews>=0.2,<0.3` → `<0.4`.

This is the release that lets a fleet install **listings 0.6.2** — the one
that closes four authorization holes on the listing surface (any
authenticated caller could `PUT`/`PATCH` any listing; `GET /{id}/` served
drafts, rejected, paused and blocked listings to anyone holding the id).
Until now `pip` answered ResolutionImpossible for that bump, with this
composite's pin as one of the two walls (the client fleet, 2026-08-22).

Nothing in the composite had to change. 0.6.0's own change is the contract
triad (`docs/{schema,flows,errors}.json`) plus a declared-type fix on two
serializers' `images`; 0.3.0 of reviews widens `GET /reviews` and
`/aggregate` to anonymous reads and throttles them from its own namespace.
`ListingReviewSummaryProjection` reads reviews' facts and the preset is
plain data — neither touches a permission class or a serializer's declared
type. Verified against listings 0.6.2 + reviews 0.3.0 in a clean venv on
released packages: full suite green, `makemigrations --check` clean,
`pip check` clean.

## [0.2.2] - 2026-08-21

### Changed — `stapel-listings` pin widens to admit 0.5

`>=0.4,<0.5` → `>=0.4,<0.6`. Verified against 0.5.0 in a clean venv on
released packages: full suite green (19/19), `makemigrations --check`
reports no missing migrations, `pip check` clean.

0.5.0's behaviour change — a live listing under re-moderation stays
`published` (only `moderation_status` moves to `pending`; `POST
.../publish/` now answers `"published"` for a live re-publish instead of
`"pending"`) — has nothing here to touch. This composite owns one
Projection over reviews' facts (`ListingReviewSummaryProjection`) plus a
plain preset (`INSTALLED_APPS`/`URL_INCLUDES` data); it never reads
`Listing.status` or `moderation_status`, so a state that was reachable by a
different path is still unreachable from a switch that does not exist.
Checked the same way 0.2.1 checked 0.4.0: nothing else in 0.5.0's CHANGELOG
touches a surface this composite consumes.

## [0.2.1] - 2026-08-21

### Changed — `stapel-listings` pin follows the fleet to 0.4

`>=0.3,<0.4` → `>=0.4,<0.5`. The composite was fixing an older combination
than the fleet ships. Verified against 0.4.0 in a clean venv on released
packages: full suite green, no missing migrations, `pip check` clean.

Nothing in the composite had to change for 0.4.0's own changes. Checked, one
by one, because a composite's job is exactly to notice:

- **The new `blocked` status / `published→blocked` takedown edge.** Nothing
  here enumerates listing statuses — the composite owns one Projection over
  reviews' facts and a preset of plain data; it never reads
  `ListingStatus`. Adding a state cannot desynchronise a switch that does not
  exist.
- **`features_search` strictly derived, `listings.search_documents` /
  `search_export`.** Listings' own comm surface; the composite declares no
  search glue (there is no search member to glue it to).
- **The `moderation.completed` consumes-schema widened target-generically.**
  This one DOES touch the composite: listings' consumer used to be
  `{listing_id}`-shaped and is now target-generic, so it shares that topic with
  reviews' consumer in this process, and each decides "is this mine?" by its
  own `MODERATION_TARGET_TYPE`. The two defaults are disjoint (`listing` vs
  `review`), so co-installation is correct out of the box — and
  `tests/test_composite.py` now holds that as a gate instead of an assumption:
  equal names would apply a review takedown to a listing sharing its key. A
  host that respells either name must configure both.

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
