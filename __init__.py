"""stapel-shop — Composite: catalog shop — categories + attributes + listings + reviews, with cross-domain glue projections.

A composite lib writes NO business logic (projections-and-composition §3):
it is an INSTALLED_APPS/urls/config preset over existing Stapel modules,
plus — where two domain-blind engines need to meet — cross-domain
``Projection`` glue declarations. The member modules stay domain-blind;
the composite is the one place allowed to know both sides.

Importable without Django settings; ``preset`` is plain data.
"""

__all__ = ["preset"]
