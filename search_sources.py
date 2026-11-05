"""The `listing` search source — cross-domain glue a composite is allowed to
write (projections-and-composition §3).

stapel-search ships ``BUILTIN_SOURCES = {}``: it knows nothing about
listings, and stapel-listings knows nothing about an index. Without a source a
host that installs search next to this composite boots with
``stapel_search.W001`` and its search page answers nothing. The pair meets
here, the same way stapel-classified declares it:

- ``listings.search_documents`` — keyed batch pull behind a ``listing.*``
  signal;
- ``listings.search_export`` — the cursor snapshot behind ``search_rebuild``;
- ``listing.published`` / ``.updated`` / ``.removed`` — identity-only
  invalidation signals; the pulled document decides visibility.

The stored card is the catalog card: title, price, currency, place, gallery
refs and publication time. Facets come from listings' ``features_search``
projection (the declared ``ACCEPT_FEATURES_SEARCH`` fallback), exactly as in
stapel-classified.

Importable without Django settings: the preset reads :data:`LISTING_SOURCE`.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any

#: The dotted path ``STAPEL_SEARCH["SOURCES"]["listing"]`` names.
LISTING_SOURCE = "stapel_shop.search_sources.listing_source"

CONTENT_FUNCTION = "listings.search_documents"
EXPORT_FUNCTION = "listings.search_export"
SIGNALS = ("listing.published", "listing.updated", "listing.removed")
REMOVAL_SIGNALS = ("listing.removed",)

#: How many gallery refs a result row carries; the detail page has the rest.
CARD_IMAGES_LIMIT = 10


def _decimal(value: Any) -> Decimal | None:
    if value in (None, ""):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _datetime(value: Any):
    if not value:
        return None
    if not isinstance(value, str):
        return value
    from django.utils.dateparse import parse_datetime

    return parse_datetime(value)


def _card(payload: dict) -> dict:
    """What a result row shows, stored with the document (no hydration hop)."""
    refs = [str(ref) for ref in (payload.get("images") or []) if ref]
    images = list(dict.fromkeys(refs))[:CARD_IMAGES_LIMIT]
    return {
        "title": payload.get("title") or "",
        "price": payload.get("price"),
        "currency": payload.get("currency") or "",
        "location_label": payload.get("location_label") or "",
        "image": images[0] if images else None,
        "images": images,
        "published_at": payload.get("published_at"),
    }


def _title_text(payload: dict) -> tuple[str, ...]:
    """Values of the ``show_at_title`` attributes, as weight-B text."""
    searchable = payload.get("features_search") or {}
    text: list[str] = []
    for dao in payload.get("features_title") or []:
        if not (isinstance(dao, dict) and dao.get("slug")):
            continue
        labels = dao.get("labels")
        values = labels if isinstance(labels, list) and labels else searchable.get(str(dao["slug"])) or []
        text.extend(str(v) for v in values if v not in (None, ""))
    return tuple(text)


def map_listing(payload: dict):
    """``listings.search_documents`` row (+ ``key``, ``seq``) -> ``SearchDocumentInput``."""
    from stapel_search.dto import SearchDocumentInput

    updated_at = _datetime(payload.get("updated_at"))
    seq = payload.get("seq")
    if seq in (None, ""):
        seq = int(updated_at.timestamp() * 1000) if updated_at else 0
    return SearchDocumentInput(
        doc_type="listing",
        doc_key=str(payload.get("key") or ""),
        status=str(payload.get("status") or ""),
        language=str(payload.get("language") or ""),
        owner_key=str(payload.get("owner_id") or ""),
        category_id=str(payload.get("category_id") or ""),
        title=str(payload.get("title") or ""),
        body=str(payload.get("description") or ""),
        text_extra=_title_text(payload),
        features_search=dict(payload.get("features_search") or {}),
        price_base=_decimal(payload.get("price_base")),
        price=_decimal(payload.get("price")),
        currency=str(payload.get("currency") or ""),
        published_at=_datetime(payload.get("published_at")),
        source_updated_at=updated_at,
        lat=_decimal(payload.get("lat")),
        lon=_decimal(payload.get("lon")),
        geohash=str(payload.get("geohash") or ""),
        location_id=str(payload.get("location_id") or ""),
        location_label=str(payload.get("location_label") or ""),
        card=_card(payload),
        seq=int(seq or 0),
    )


def listing_source():
    """The ``SourceSpec`` behind :data:`LISTING_SOURCE`.

    ``visible_statuses`` is read from stapel-listings, so a lifecycle state
    added there cannot leave the index's idea of "live" behind.
    """
    from stapel_listings.models import INDEXED_STATUSES
    from stapel_search.registry import SourceSpec

    return SourceSpec(
        doc_type="listing",
        mapper=map_listing,
        content_function=CONTENT_FUNCTION,
        export_function=EXPORT_FUNCTION,
        signals=SIGNALS,
        removal_signals=REMOVAL_SIGNALS,
        key_fields=("listing_id", "key"),
        visible_statuses=frozenset(str(status) for status in INDEXED_STATUSES),
    )


__all__ = [
    "CONTENT_FUNCTION",
    "EXPORT_FUNCTION",
    "LISTING_SOURCE",
    "REMOVAL_SIGNALS",
    "SIGNALS",
    "listing_source",
    "map_listing",
]
