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
      fresh ``aggregate`` — event-carried state transfer).

    Known gaps against stapel-reviews 0.1.0 (declared with the CANONICAL
    names; loud failures until reviews ships them — see README):

    - ``reviews.aggregates_by_keys`` (keyed batch live query,
      ``{"keys": [...]}`` → ``{key: {"avg", "count"}}``) does not exist yet —
      local-mode ``read()`` raises FunctionNotRegistered. reviews today has
      only the single-target ``reviews.aggregate``.
    - ``reviews.aggregates_export`` (cursor-paged snapshot for ``rebuild``)
      does not exist yet — remote-mode rebuild fails loudly.
    - reviews' facts carry EVERY target_type; in remote mode ``apply()``
      would also upsert non-listing targets (harmless extra rows keyed by
      their target_key, never joined to a listing). Payload filtering in the
      Projection primitive (or per-type topics in reviews) is the clean fix.
    """

    name = "shop.listing_review_summary"
    consumes = ("reviews.review.published", "reviews.review.hidden")
    model = "shop.ListingReviewSummary"            # used in remote mode only
    source_key = "target_key"                      # == listing id for "listing" targets
    live_query = "reviews.aggregates_by_keys"      # NEEDED in stapel-reviews
    source_of_truth = "reviews.aggregates_export"  # NEEDED in stapel-reviews

    def apply(self, event):
        agg = event.payload.get("aggregate") or {}
        return {
            "rating_avg": float(agg.get("avg", 0.0)),
            "rating_count": int(agg.get("count", 0)),
        }
