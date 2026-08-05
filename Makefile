PYTHON ?= python3

.PHONY: contract contract-check

# First: the `surface` section of docs/capabilities.json — the symbols a
# product is meant to CALL (discoverability-design.md §1.2). This module
# declares an EMPTY surface_roots in docs/capabilities.meta.json: it is a
# thin composite preset (plain INSTALLED_APPS/URL_INCLUDES data plus one
# Projection class with no annotated fields) with no usage surface of its
# own to publish — `--patch` still refreshes module/version every run.
#
# NOTE the rest of docs/capabilities.json is still HAND-AUTHORED (no
# schema/flows/errors triad emitter exists — see git log: "author
# capabilities.json for the stapel-catalog sweep") and this step never
# touches provides/axes/extension_points/requires.
#
# Second: docs/llms.txt, the fifth contract artifact (stapel_tools.llms_txt —
# the module's own context slice for an agent; badge-canon §3), rendered
# straight from the docs/capabilities.json the step above produces.
contract:
	$(PYTHON) -m stapel_tools.surface . --patch
	$(PYTHON) -m stapel_tools.llms_txt . --out docs

# Drift gate: llms_txt's own --check mode compares a fresh render (from the
# committed docs/capabilities.json) against the committed docs/llms.txt.
contract-check:
	$(PYTHON) -m stapel_tools.surface . --patch --check
	$(PYTHON) -m stapel_tools.llms_txt . --check
