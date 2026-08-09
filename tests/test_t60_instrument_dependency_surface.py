"""T60 - which third-party modules each served instrument needs, AS A TESTED
FACT rather than a table in a dispatch (E31 task 2).

WHY IT MATTERS. The eight served tools do not share a dependency set, and the
split is a design lever: FOUR need `open3d` and FOUR do not, and the four that
do not include BOTH anchor tools - the half [E14 Ruling 35]'s per-profile
anchor gate calls. Measured at E31 on a clean install: with `numpy scipy
trimesh pillow` present and `open3d` absent, 4 of 8 served tools return
payloads. That number is only usable if the split cannot drift silently, so it
is pinned here.

AND `open3d` IS THE ONE THAT CANNOT ALWAYS BE HAD. Measured from the index at
E31: `open3d` 0.19.0 - the latest release - publishes cp310/cp311/cp312 wheels
and NOTHING for cp313 or later, while `pyproject.toml` declares
`requires-python = ">=3.11"`. On the rig's own Python 3.13 `pip install
open3d` reports "no matching distribution" - there is no sdist either. A
dependency group that hard-requires it would fail on a Python this package
says it supports.

MODULE LEVEL IS THE UNIT, and it is the right one: an instrument is invoked as
a SUBPROCESS, so a module-level import decides whether the tool can run at
all, while a function-level import decides only whether one branch can. That
distinction is not academic here - `verify/anchor_compare.py` imports PIL and
numpy INSIDE functions, which is why `anchor_check` is the only served tool
that answers on an install with no third-party dependency at all.

Everything printed here is ASCII (the repo's law).
"""
import ast
import os

import pytest

from conftest import TOOLS

# The third-party names this repo's instruments can import. Anything outside
# this set is stdlib or a repo sibling; `subject_profile` is deliberately
# listed as a SIBLING because it is the fourth failure class E31 found - a
# repo module that packaging the two instrument directories does not ship.
THIRD_PARTY = {"numpy", "scipy", "trimesh", "PIL", "open3d", "cv2", "mcp"}
SIBLINGS = {"subject_profile", "facet_index"}

# The wrapped instrument behind each served tool, from spec 2's table. Written
# out rather than imported from measure_mcp, so a change there fails HERE too
# instead of quietly re-pointing the assertions at itself.
WRAPPED = {
    "mesh_stats": "verify/mesh_stats.py",
    "mesh_topology": "diagnostics/e14_topology.py",
    "reach_ceiling": "diagnostics/e08_ceiling.py",
    "thin_extent_curve": "diagnostics/e12_thin_curve.py",
    "offsurface_rate": "diagnostics/e12_offsurface.py",
    "texel_provenance": "diagnostics/texel_provenance.py",
    "anchor_check": "verify/anchor_compare.py",
    "measure_report": "verify/gate1_sheet.py",
}

# MEASURED at E31 by reading every import statement of the eight, then
# CONFIRMED by installing each tier into a clean venv and calling all eight.
NEEDS_OPEN3D = {"reach_ceiling", "thin_extent_curve", "offsurface_rate",
                "texel_provenance"}
NEEDS_NOTHING = {"anchor_check"}


def module_level_imports(path):
    """Top-level import names only - the ones that decide whether `python
    <script>.py` can start at all. A function-level import is a different
    question and is measured separately below."""
    with open(path, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    names = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            names.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module.split(".")[0])
    return names


def nested_imports(path):
    """Imports that are NOT at module level - inside a function, a class, or
    any block. These are the lazy ones."""
    with open(path, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    top = set(id(n) for n in tree.body)
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)) and id(node) not in top:
            if isinstance(node, ast.Import):
                names.update(a.name.split(".")[0] for a in node.names)
            elif node.module:
                names.add(node.module.split(".")[0])
    return names


def instrument(rel):
    return str(TOOLS / rel.replace("/", os.sep))


# ---------------------------------------------------------------------------
# the can-fail leg, on a SYNTHETIC file
# ---------------------------------------------------------------------------

def test_t60_the_scanner_separates_module_level_from_nested(tmp_path):
    """THE CAN-FAIL LEG. A scanner that returned everything, or nothing, would
    make every pin below meaningless. The fixture names a module that does not
    exist anywhere in this repo, because E28 measured a fixture naming a REAL
    module moving the very count it was verifying."""
    src = tmp_path / "synthetic_probe_module.py"
    src.write_text(
        "import zzz_top_level_only\n"
        "from zzz_top_from import thing\n"
        "def f():\n"
        "    import zzz_nested_only\n"
        "    return zzz_nested_only, thing\n", encoding="ascii")
    top = module_level_imports(str(src))
    nested = nested_imports(str(src))
    assert top == {"zzz_top_level_only", "zzz_top_from"}, top
    assert nested == {"zzz_nested_only"}, nested
    assert "zzz_nested_only" not in top, (
        "a nested import read as module level - the whole distinction this "
        "file rests on would be gone")


# ---------------------------------------------------------------------------
# the split
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tool", sorted(WRAPPED))
def test_t60_the_open3d_split_is_four_and_four(tool):
    """FOUR of the eight need open3d at module level and FOUR do not. The lever
    is the second half: a tier without open3d still serves both anchor tools,
    `mesh_stats` and `mesh_topology`."""
    top = module_level_imports(instrument(WRAPPED[tool]))
    has = "open3d" in top
    assert has == (tool in NEEDS_OPEN3D), (
        "%s (%s) %s open3d at module level; the split this repo reasons about "
        "has moved and every tiering claim made from it is stale"
        % (tool, WRAPPED[tool], "now imports" if has else "no longer imports"))


def test_t60_exactly_four_need_open3d():
    """The count itself, so a change that swaps which four still fires."""
    got = {t for t in WRAPPED
           if "open3d" in module_level_imports(instrument(WRAPPED[t]))}
    assert got == NEEDS_OPEN3D, sorted(got ^ NEEDS_OPEN3D)
    assert len(got) == 4


def test_t60_anchor_compare_needs_nothing_at_module_level():
    """WHY `anchor_check` IS THE OUTLIER. Its instrument imports PIL and numpy
    inside functions, so the byte tier - sha256 over two files - runs on the
    standard library alone. E31 measured it returning a payload from an install
    carrying `mcp` and nothing else.

    Moving either import to module level would close that door, and it would
    close it silently, because every rig this repo runs on has both.
    """
    path = instrument(WRAPPED["anchor_check"])
    top = module_level_imports(path)
    assert not (top & THIRD_PARTY), (
        "anchor_compare now imports %s at module level; the one served tool "
        "that works on a dependency-free install has stopped working"
        % sorted(top & THIRD_PARTY))
    assert {"PIL", "numpy"} <= nested_imports(path), (
        "the lazy imports moved or were removed - re-measure what the byte "
        "tier costs before trusting the claim above")


@pytest.mark.parametrize("tool", sorted(WRAPPED))
def test_t60_every_third_party_import_is_a_named_one(tool):
    """No served instrument may acquire a dependency nobody has declared. E23's
    CI gate fired on exactly this - a module-level `cv2` in a route tool no
    test had ever invoked - and a new name here would reach a user as an
    INSTRUMENT_FAILED with a traceback in its hint."""
    top = module_level_imports(instrument(WRAPPED[tool]))
    external = {n for n in top
                if n not in SIBLINGS and not _is_stdlib(n)}
    assert external <= THIRD_PARTY, (
        "%s imports %s, which is not in this file's declared set - add it "
        "deliberately, with the dependency declaration it implies"
        % (tool, sorted(external - THIRD_PARTY)))


def _is_stdlib(name):
    import sys
    return name in sys.stdlib_module_names


def test_t60_mesh_stats_reaches_a_repo_sibling_not_only_third_parties():
    """THE FOURTH FAILURE CLASS, pinned. `verify/mesh_stats.py` imports
    `subject_profile`, a module in `tools/` - so packaging `diagnostics/` and
    `verify/` is NOT sufficient to make it run from an install. Measured at
    E31: with both instrument directories shipped and `subject_profile` left
    behind, mesh_stats died on `No module named 'subject_profile'`, a different
    defect from every other tool's missing `numpy`."""
    top = module_level_imports(instrument(WRAPPED["mesh_stats"]))
    assert "subject_profile" in top, (
        "mesh_stats no longer imports subject_profile - the packaging note "
        "that depends on it is stale")
    assert (TOOLS / "subject_profile.py").exists()
    assert not (TOOLS / "verify" / "subject_profile.py").exists(), (
        "subject_profile moved into an instrument directory; the packaging "
        "gap this leg records has changed shape")
