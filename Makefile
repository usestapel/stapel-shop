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
#
# Third: assemble README.md (stapel_tools.readme) from docs/readme.md — the
# human half, the only file a person edits — plus the artifacts above. The
# badge row, the version, the fact table and every doc link are generated,
# so they cannot lag a release the way a hand-written README always has.
contract:
	$(PYTHON) -m stapel_tools.surface . --patch
	$(PYTHON) -m stapel_tools.llms_txt . --out docs
	$(PYTHON) -m stapel_tools.readme .

# Drift gate: llms_txt's own --check mode compares a fresh render (from the
# committed docs/capabilities.json) against the committed docs/llms.txt;
# readme --check compares a fresh render against the committed README.md.
contract-check:
	$(PYTHON) -m stapel_tools.surface . --patch --check
	$(PYTHON) -m stapel_tools.llms_txt . --check
	$(PYTHON) -m stapel_tools.readme . --check
