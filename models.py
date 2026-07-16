"""Remote-mode read-model tables for the shop composite's glue.

Only materialised when the projection resolves to REMOTE mode (owner module
not installed in this process); in the composite's normal monolith shape the
table stays empty/unused (local mode reads live through the owner).
"""
from django.db import models

from stapel_core.django.projections.models import ProjectionModel


class ListingReviewSummary(ProjectionModel):
    """Per-listing rating aggregate projected from reviews' facts.

    ``projection_key`` == the review target_key (the listing id). Read it
    through ``stapel_core.comm.projections.read("shop.listing_review_summary",
    keys=[...])`` — never via the ORM directly (that hard-wires remote mode).
    """

    rating_avg = models.FloatField(default=0.0)
    rating_count = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = "shop"

    def __str__(self):
        return f"listing {self.projection_key}: {self.rating_avg} ({self.rating_count})"
