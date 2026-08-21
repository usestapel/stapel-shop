"""Drift gate for the `surface` section of ``docs/capabilities.json``.

Unlike most modules in this sweep, stapel-shop declares an EMPTY
``surface_roots`` in ``docs/capabilities.meta.json``: it is a thin composite
preset (``preset.py``'s ``INSTALLED_APPS``/``URL_INCLUDES``/
``SETTINGS_DEFAULTS`` are plain data, not selectable symbols) plus one
``Projection`` class whose fields are plain assignments rather than annotated
ones, so the ``capability_fields`` selector would pick up nothing there
either. This module genuinely has no usage surface of its own to publish —
see the ``_comment`` in ``docs/capabilities.meta.json`` for the reasoning, and
do not "fix" this test by inventing a root.

``--patch`` still refreshes ``module``/``version`` from ``pyproject.toml`` on
every run, and an empty ``surface_roots`` with a non-empty curated ``surface``
map would fail emission as stale prose — this test only guards against THAT
drift, not against a nonexistent surface list.

Honest boundary: the REST of this module's ``capabilities.json`` is still
hand-written (no schema/flows/errors triad emitter), so only
``module``/``version``/``surface`` are gated below.
"""
import json
from pathlib import Path

import pytest

try:
    import stapel_tools  # noqa: F401  (probe: the emitter must be importable)
except ImportError as exc:  # pragma: no cover - environment failure, not a branch
    # NOT pytest.importorskip. A drift gate that skips when its emitter is
    # missing reports `1 skipped`, exits 0, and disappears among a hundred
    # green tests. A gate that cannot run has FAILED; it has not passed.
    raise RuntimeError(
        "capabilities surface drift gate cannot run: stapel-tools is not "
        "importable, and it carries the capabilities emitter this gate "
        "measures drift against. Install it (workspace venv, or `pip install "
        "stapel-tools`) and re-run. This is a hard failure on purpose — a "
        "skipped drift gate is silently no gate."
    ) from exc

from stapel_tools.surface import _stable_json, load_meta, patch_capabilities  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
COMMITTED = REPO / "docs" / "capabilities.json"


def _emitted() -> dict:
    try:
        return patch_capabilities(REPO, load_meta(REPO))
    except SystemExit as exc:  # the LOUD rule — report it, don't bury it
        pytest.fail(f"capabilities emission refused: {exc}", pytrace=False)


def test_no_drift():
    assert COMMITTED.read_text() == _stable_json(_emitted()), (
        "docs/capabilities.json is stale — run `make contract` and commit it"
    )


def test_version_tracks_pyproject():
    """The document carries the module version, refreshed from pyproject.toml
    by --patch on every `make contract` run."""
    import tomllib

    pyproject = tomllib.loads((REPO / "pyproject.toml").read_text())
    assert json.loads(COMMITTED.read_text())["version"] == (
        pyproject["project"]["version"]
    )


def test_surface_is_honestly_empty():
    """An EMPTY `surface` list, not an absent key — stapel_tools.surface's
    ``patch_capabilities`` writes ``[]`` when the meta layer declares a
    ``no_surface`` reason, precisely so "declared none" (this module) and
    "nobody has filled this in yet" (an absent key) don't look identical to
    a downstream reader (the fleet aggregate, the llms.txt renderer, ...).
    See ``docs/capabilities.meta.json``'s `no_surface` for the reasoning."""
    doc = json.loads(COMMITTED.read_text())
    assert doc.get("surface") == []
