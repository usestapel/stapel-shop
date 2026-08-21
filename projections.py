"""Cross-domain glue of the shop composite (projections-and-composition §3).

reviews is target-generic — it must not know listings exist; listings must
not know reviews exist. The composite is the one place allowed to know both
sides, so the reviews→listings Projection lives HERE, not in either module.
"""
from stapel_core.comm import Projection


class ListingReviewSummaryProjection(Projection):
    """Per-listing rating aggregate, owned by reviews (reviews → listings).

    One declaration, two modes (stapel-core §1 colocation semantics):

    - local (monolith — reviews installed next to this app, the composite's
      normal shape): no table, no bus subscription; ``read()`` goes through
      the owner's keyed ``live_query`` Function.
    - remote (reviews split into its own service): the ListingReviewSummary
      table is fed from reviews' visibility facts
      (``reviews.review.published`` / ``reviews.review.hidden`` carry the
      fresh ``aggregate`` — event-carried state transfer), and ``rebuild()``
      re-derives it from the owner's cursor-paged export.

    **One shape in both modes** (``read()`` contract in stapel-core:
    "identical shape in both modes"). Local mode hands back whatever the
    owner's ``live_query`` returns — stapel-reviews answers ``{"avg",
    "count"}`` — and stapel-core has no hook to rename those on the way out.
    So the owner's names ARE the contract shape here, and the read-model
    columns carry the same two names; ``apply()`` / ``from_snapshot()`` map
    the owner's two wire shapes onto them:

        read("shop.listing_review_summary", keys=["42"])
        # {"42": {"avg": 4.5, "count": 12}}   — local AND remote

    Wire shapes this is written against (stapel-reviews >= 0.2, the versions
    that first shipped both Functions):

    - ``reviews.aggregates_by_keys`` (``live_query``) — ``{"keys": [str, ...]}``
      → ``{key: {"avg": float, "count": int}}``. A key with no published
      review is ABSENT from the answer (not present with zeros), per the
      ``live_query`` contract.
    - ``reviews.aggregates_export`` (``source_of_truth``) —
      ``{"cursor": str|None, "limit": int}`` → ``{"rows": [...], "cursor":
      <next|None>, "total": <int|None>}``, the shape
      ``stapel_core.comm.projections._iter_snapshot`` pages through (it reads
      ``resp["rows"]``, NOT ``items``). Each row is ``{"target_key",
      "target_type", "avg", "count", "seq"}``; ``seq`` is unix milliseconds —
      the same clock an Event timestamp uses, which is what lets a live fact
      arriving mid-rebuild outrank the snapshot row instead of racing it
      (this projection declares no ``sequence_field``, so a live event is
      positioned by its timestamp — same unit, comparable).
    - ``reviews.review.published`` / ``.hidden`` facts carry ``target_key``
      (the ``source_key``) and a fresh ``aggregate`` of the same
      ``{"avg", "count"}``.

    Known gap: reviews' facts and its export carry EVERY target_type; in
    remote mode both ``apply()`` and ``rebuild()`` also materialise
    non-listing targets (harmless extra rows keyed by their target_key, never
    joined to a listing). Payload filtering in the Projection primitive (or
    per-type topics in reviews) is the clean fix.
    """

    name = "shop.listing_review_summary"
    consumes = ("reviews.review.published", "reviews.review.hidden")
    model = "shop.ListingReviewSummary"            # used in remote mode only
    source_key = "target_key"                      # == listing id for "listing" targets
    live_query = "reviews.aggregates_by_keys"      # {"keys": [...]} -> {key: {avg, count}}
    source_of_truth = "reviews.aggregates_export"  # {cursor, limit} -> {rows, cursor, total}

    def apply(self, event):
        """Fact → row fields. The fresh aggregate rides on the event."""
        return self._fields(event.payload.get("aggregate") or {})

    def from_snapshot(self, row):
        """Export row → row fields.

        Required, not optional: an export row carries ``target_type`` and the
        owner's ``avg``/``count``, and the base implementation drops only
        ``target_key``/``seq`` — feeding the rest to the model would raise
        ``TypeError: unexpected keyword argument 'target_type'``.
        """
        return self._fields(row)

    @staticmethod
    def _fields(aggregate):
        """The read-model columns, from either of the owner's two shapes."""
        return {
            "avg": float(aggregate.get("avg") or 0.0),
            "count": int(aggregate.get("count") or 0),
        }
