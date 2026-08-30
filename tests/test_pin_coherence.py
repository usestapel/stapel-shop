"""Pin-coherence gate — a composite's one real failure mode.

This package writes no business logic: its whole product is a *combination*
of member versions. Every release since 0.2.4 fixed the same defect — a cap
here excluded a member version the fleet had to install, and pip answered
`ResolutionImpossible` rather than warning, so the composite was the wall.
0.2.7 is the fourth: `stapel-attributes<0.5` while stapel-categories 0.7.0
requires `stapel-attributes>=0.5,<1.0` has no solution at all.

Nothing in this repo's code could catch that, because no code here reads a
member's surface — the contradiction lives entirely in metadata. So the gate
reads metadata:

1. this package's own specifiers must admit the member versions that are
   actually installed (the versions the rest of this suite just ran against —
   a green suite against a version the wheel forbids is not a release);
2. every member's own requirement on a fellow stapel distribution must be
   satisfied by that same installed set, so the combination this composite
   fixes is one pip can actually resolve.

Where it fires: in a workspace holding the released siblings (editable
checkouts at their tags), a stale cap here fails (1) immediately. In CI, pip
resolved the environment from these very specifiers, so both hold by
construction unless a git-main member has outgrown a cap — which is the same
finding one release earlier.
"""
import tomllib
from importlib.metadata import PackageNotFoundError, distribution
from importlib.metadata import version as installed_version
from pathlib import Path

from packaging.requirements import Requirement

REPO = Path(__file__).resolve().parent.parent
DIST = "stapel-shop"


def _canon(name: str) -> str:
    return name.lower().replace("_", "-")


def _own_requirements() -> list[Requirement]:
    """This package's dependencies, read from the repo's pyproject.toml.

    Deliberately the source file and not `importlib.metadata`: the file is
    what the release publishes, while installed metadata can lag behind an
    edit until the editable install is refreshed.
    """
    pyproject = tomllib.loads((REPO / "pyproject.toml").read_text())
    return [Requirement(spec) for spec in pyproject["project"]["dependencies"]]


def _member_names() -> list[str]:
    return [_canon(req.name) for req in _own_requirements()]


def _requirements_of(dist_name: str) -> list[Requirement]:
    try:
        raw = distribution(dist_name).requires or []
    except PackageNotFoundError:  # pragma: no cover - guarded by the caller
        return []
    return [Requirement(spec) for spec in raw]


def _installed(name: str) -> str | None:
    try:
        return installed_version(name)
    except PackageNotFoundError:
        return None


def test_pins_admit_the_installed_members():
    """Every member this composite pins, at the version the suite ran against."""
    missing = []
    violations = []
    for req in _own_requirements():
        version = _installed(req.name)
        if version is None:
            missing.append(req.name)
            continue
        if not req.specifier.contains(version, prereleases=True):
            violations.append(f"{req.name} {version} is excluded by '{req}'")

    assert not missing, (
        "composite members are not installed, so this gate measured nothing: "
        + ", ".join(sorted(missing))
    )
    assert not violations, (
        "pyproject.toml forbids a member version this suite ran against — the "
        "wheel would make it unresolvable for every consumer:\n  "
        + "\n  ".join(sorted(violations))
    )


def test_members_requirements_agree_with_the_installed_set():
    """No member demands a fellow member version the installed set does not hold.

    This is the second half of the same question: a cap here can be perfectly
    self-consistent and still contradict what a member itself requires (0.7.0
    of stapel-categories requires `stapel-attributes>=0.5`). Only stapel
    distributions are examined — third-party pins are the members' own business.
    """
    members = _member_names()
    violations = []
    for member in members:
        if _installed(member) is None:
            continue
        for req in _requirements_of(member):
            name = _canon(req.name)
            if not name.startswith("stapel-") or req.marker is not None:
                continue
            version = _installed(name)
            if version is None:
                continue
            if not req.specifier.contains(version, prereleases=True):
                violations.append(
                    f"{member} {_installed(member)} requires '{req}', "
                    f"but {name} {version} is installed"
                )

    assert not violations, (
        "the pinned combination does not resolve — a member's own requirement "
        "conflicts with the installed version of another member:\n  "
        + "\n  ".join(sorted(violations))
    )
