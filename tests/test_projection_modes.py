"""The reviews→listings glue projection, exercised against the REAL producer.

stapel-reviews >= 0.2 ships both halves this projection is declared against
(``reviews.aggregates_by_keys`` as ``live_query``,
``reviews.aggregates_export`` as ``source_of_truth``), so nothing here is
mocked: the same review rows are read live through the owner (local mode) and
rebuilt into the table from the owner's export (remote mode), and the two
answers have to be the same shape — stapel-core's ``read()`` contract says
"identical shape in both modes".
"""
import pytest
from stapel_core.bus.event import Event
from stapel_core.comm.projections import (
    apply_event,
    projection_registry,
    read,
    rebuild,
    resolve_mode,
)

NAME = "shop.listing_review_summary"

#: One row exactly as ``reviews.aggregates_export`` serves it (stapel-reviews
#: 0.2.0 ``services.aggregates_export``): the ``source_key``, the target type
#: that must NOT reach the model's constructor, the owner's field names, and a
#: ``seq`` in unix milliseconds.
EXPORT_ROW = {
    "target_key": "listing-42",
    "target_type": "listing",
    "avg": 4.5,
    "count": 12,
    "seq": 1_754_000_000_000,
}

KEYS = ["listing-42", "listing-7", "listing-never-reviewed"]


@pytest.fixture
def proj():
    return projection_registry.get(NAME)


@pytest.fixture
def remote(proj, monkeypatch):
    """The remote topology, forced inside this monolithic test process."""
    monkeypatch.setattr(proj, "force_mode", "remote")
    return proj


@pytest.fixture
def published_reviews(db):
    """Two published reviews of one listing, one of another — the owner's rows."""
    from django.contrib.auth import get_user_model
    from stapel_reviews.models import Review, ReviewStatus

    author = get_user_model().objects.create(username="reviewer")
    for rating in (4, 5):
        Review.objects.create(
            target_type="listing", target_key="listing-42", author=author,
            rating=rating, status=ReviewStatus.PUBLISHED,
        )
    Review.objects.create(
        target_type="listing", target_key="listing-7", author=author,
        rating=2, status=ReviewStatus.PUBLISHED,
    )
    return author


EXPECTED = {
    "listing-42": {"avg": 4.5, "count": 2},
    "listing-7": {"avg": 2.0, "count": 1},
    # "listing-never-reviewed" is ABSENT — the live_query contract, and the
    # difference between "nobody rated it" and "everybody rated it 0".
}


def test_from_snapshot_maps_an_export_row_onto_the_model(proj):
    """``rebuild()`` feeds ``from_snapshot(row)`` straight into the model, so
    the row's ``target_type`` (and the owner's field names) must be mapped —
    the inherited default would only drop ``target_key``/``seq`` and blow up
    with an unexpected keyword argument."""
    from stapel_shop.models import ListingReviewSummary

    fields = proj.from_snapshot(EXPORT_ROW)
    assert fields == {"avg": 4.5, "count": 12}

    row = ListingReviewSummary(
        projection_key=EXPORT_ROW["target_key"],
        projection_seq=EXPORT_ROW["seq"],
        projection_event_id="",
        **fields,
    )
    assert (row.avg, row.count) == (4.5, 12)


def test_local_read_goes_through_the_owners_live_query(proj, published_reviews):
    assert resolve_mode(proj) == "local"  # stapel_reviews is installed here
    assert read(NAME, KEYS) == EXPECTED


def test_remote_rebuild_reads_the_owners_export(remote, published_reviews):
    """The export answers ``{rows, cursor, total}`` — what core's
    ``_iter_snapshot`` pages through — and its per-row ``seq`` seeds the row's
    sequence, so a live fact that lands after a rebuild still wins."""
    from stapel_shop.models import ListingReviewSummary

    result = rebuild(NAME)
    assert (result.rows, result.batches) == (2, 1)
    assert read(NAME, KEYS) == EXPECTED
    assert ListingReviewSummary.objects.get(projection_key="listing-42").projection_seq > 0


def test_remote_apply_upserts_the_fact_and_rejects_a_stale_one(remote, db):
    fresh = Event(
        event_type="reviews.review.published",
        service="reviews",
        payload={
            "target_type": "listing",
            "target_key": "listing-42",
            "aggregate": {"avg": 4.5, "count": 12},
        },
    )
    assert apply_event(remote, fresh) == "created"
    assert read(NAME, ["listing-42"]) == {"listing-42": {"avg": 4.5, "count": 12}}

    stale = Event(
        event_type="reviews.review.hidden",
        service="reviews",
        payload={
            "target_type": "listing",
            "target_key": "listing-42",
            "aggregate": {"avg": 1.0, "count": 1},
        },
        timestamp=fresh.timestamp - 1000,
    )
    assert apply_event(remote, stale) == "skipped"
    assert read(NAME, ["listing-42"]) == {"listing-42": {"avg": 4.5, "count": 12}}


def test_both_modes_answer_the_same_shape(proj, monkeypatch, published_reviews):
    """The whole point of the single ``read()`` accessor: business code that
    works in the monolith keeps working when reviews is split out."""
    local_answer = read(NAME, KEYS)
    assert resolve_mode(proj) == "local"

    monkeypatch.setattr(proj, "force_mode", "remote")
    rebuild(NAME)
    remote_answer = read(NAME, KEYS)

    assert remote_answer == local_answer
    assert {k: sorted(v) for k, v in remote_answer.items()} == {
        "listing-42": ["avg", "count"],
        "listing-7": ["avg", "count"],
    }
