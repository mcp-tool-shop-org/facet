"""T63 - the packaging decision, held in place.

E31 measured that `pip install facet-mcp` gave a record server and NO
measurement server: the wheel held two `.py` files, and the eight served tools
invoke instruments as SUBPROCESSES, so there was nothing to invoke. Six tiers,
each an actual wheel in its own clean venv, ended at 0-of-8 failing. E31
Ruling 6 adopted Shape A - the instruments ship - at the Director's word that
facet-measure ships.

WHAT THIS FILE PINS: the structural facts that, if any one of them is quietly
undone, put the wheel back to 8-of-8 failing without a single test going red
anywhere else. Every assertion here is cheap and hermetic.

WHAT IT DELIBERATELY DOES NOT DO, stated rather than left to be discovered:
it does not build a wheel or create a venv. That measurement is E31's arc
evidence - six tiers, recorded with their sizes and per-tool verdicts in
E31-publish-the-pipeline-report.md - and it needs the network and several
hundred megabytes. Re-running it on every commit is not what "tests ride the
commit" asks for. What CAN silently regress is the declaration and the path
expression, and those are what this file holds.

Layer 0 (the module in the artifact) is pinned by T59; the transport by T58;
the dependency split by T60; the frozen-binary refusal by T61; the recorded
invocation form by T62. This file is the join: does the thing the server
invokes actually travel with it.
"""

import importlib.util
import os
import re
import sys
import tomllib

import pytest

from conftest import REPO, TOOLS


@pytest.fixture(scope="module")
def measure_mcp():
    """measure_mcp imported in-process, the `facet_index_mod` pattern.

    Its module level is constants, function defs and the MCPServer
    construction - no instrument runs at import, which is the property
    `tools/*/__init__.py` being code-free also protects. `tools/` goes on
    sys.path first because measure_mcp imports facet_index at module level,
    exactly as an install would resolve it beside itself.
    """
    if str(TOOLS) not in sys.path:
        sys.path.insert(0, str(TOOLS))
    spec = importlib.util.spec_from_file_location(
        "measure_mcp", str(TOOLS / "measure_mcp.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _pyproject():
    with open(os.path.join(str(REPO), "pyproject.toml"), "rb") as fh:
        return tomllib.load(fh)


def _packaged_dirs():
    return set(_pyproject().get("tool", {}).get("setuptools", {})
               .get("packages", []))


def _wrapped_rels():
    """Every instrument path the server can hand to `run_instrument`, read
    from the module's own registry rather than re-listed here - a second copy
    of that list is a second population that drifts from the first."""
    src = (TOOLS / "measure_mcp.py").read_text(encoding="utf-8")
    return sorted({m.group(1) for m in
                   re.finditer(r"run_instrument\(\s*[\"']([^\"']+)[\"']", src)})


# ---------------------------------------------------------------------------
# the join: what the server invokes must be what the wheel carries
# ---------------------------------------------------------------------------

def test_t63_the_registry_is_not_empty():
    """The can-fail leg for every parametrized test below. A regex that stops
    matching would silently turn each of them into a pass over an empty set -
    the exact 'check that cannot fail' this repo keeps paying for."""
    rels = _wrapped_rels()
    assert len(rels) >= 6, (
        "found only %d run_instrument call sites; the registry reader is "
        "broken and every leg below is vacuous" % len(rels))


@pytest.mark.parametrize("rel", _wrapped_rels())
def test_t63_every_invoked_instrument_lives_in_a_packaged_directory(rel):
    """THE ONE THAT MATTERS. An instrument the server can invoke, sitting in a
    directory pyproject does not package, is a tool that works in a checkout
    and fails on every installed machine - which is precisely the defect E31
    found, and it was invisible here because this repo IS the checkout."""
    top = rel.replace("\\", "/").split("/")[0]
    assert top in _packaged_dirs(), (
        "measure_mcp invokes %s, but pyproject does not package %r "
        "(packages = %r). An install would have nothing to invoke."
        % (rel, top, sorted(_packaged_dirs())))


@pytest.mark.parametrize("rel", _wrapped_rels())
def test_t63_every_invoked_instrument_exists_on_disk(rel):
    assert (TOOLS / rel.replace("/", os.sep)).exists(), (
        "measure_mcp invokes %s and no such file exists" % rel)


def test_t63_packaging_needs_no_init_py_and_the_route_never_imports_these():
    """The reason `__init__.py` is absent, pinned so it is not re-added by
    someone reasoning from habit.

    A first draft of this arc added both marker files, on the assumption that
    a `packages` entry needs one. It does not: measured on clean builds, the
    wheel carries 99 + 9 either way and an installed `mesh_stats` runs from a
    clean venv either way. And the files are not harmless - the census keys
    axes D/E/G on the filename, so `__init__.py` in both homes fires its
    duplicate-basename ANDON, which is exactly what happened.

    The deeper reason is the one worth keeping: **nothing imports these
    directories.** `tool_path` builds a filesystem path and the server spawns
    the instrument as a subprocess, so package-ness is not a property this
    route needs from them.
    """
    for d in sorted(_packaged_dirs()):
        assert not (TOOLS / d / "__init__.py").exists(), (
            "tools/%s/__init__.py is back - packaging does not need it and it "
            "fires the census's duplicate-basename ANDON (see T62)" % d)
    src = (TOOLS / "measure_mcp.py").read_text(encoding="utf-8")
    for d in sorted(_packaged_dirs()):
        assert ("import %s" % d) not in src, (
            "measure_mcp now imports %r; these directories are spawned as "
            "subprocesses by path, and importing one would run a "
            "straight-line module-level script" % d)


# ---------------------------------------------------------------------------
# the path expression - resolved beside the module, never via REPO
# ---------------------------------------------------------------------------

def test_t63_tool_path_resolves_beside_the_module_not_via_repo(measure_mcp):
    """E24's fix is the WRONG remedy for this question and that distinction is
    the whole repair. RECORD_MARKERS key on the CORPUS, which cannot ship;
    instruments are code and do. A tool_path built from REPO pointed at
    `<venv>\\Lib\\tools\\...` - outside the package entirely."""
    m = measure_mcp
    got = m.tool_path("verify/mesh_stats.py")
    assert got == os.path.join(m.HERE, "verify", "mesh_stats.py")
    assert os.path.exists(got)
    assert "tools" not in os.path.relpath(got, m.HERE).split(os.sep), (
        "tool_path re-introduced a 'tools' segment relative to the module; in "
        "an install there is no such directory")


def test_t63_tool_path_accepts_both_recorded_spellings(measure_mcp):
    """`run_instrument` passes `verify/x.py`; the envelope records
    `tools/verify/x.py`. Both must land on the same file or a payload can
    certify a sha256 for an instrument it did not execute."""
    m = measure_mcp
    assert m.tool_path("verify/mesh_stats.py") == \
        m.tool_path("tools/verify/mesh_stats.py")


def test_t63_the_envelope_hashes_the_file_that_ran(measure_mcp):
    """Two different path expressions for one file is how the identity
    envelope - the server's whole claim to comparability - comes to describe
    something other than what executed."""
    m = measure_mcp
    src = (TOOLS / "measure_mcp.py").read_text(encoding="utf-8")
    assert "_sha256_file(tool_path(instrument_rel))" in src, (
        "the envelope no longer builds its path with tool_path; if it "
        "constructs one itself the two can disagree")


# ---------------------------------------------------------------------------
# the refusal that makes a four-of-eight install usable
# ---------------------------------------------------------------------------

def test_t63_missing_dependency_refuses_rather_than_erroring(measure_mcp):
    """An absent dependency is the ENVIRONMENT failing to answer, not the
    instrument breaking - so it is exit 4 REFUSED, the code this repo reserves
    for the tool working and telling you not to proceed."""
    m = measure_mcp
    assert m.CODES["MISSING_DEPENDENCY"] == m.facet_index.EXIT_REFUSED
    assert m.CODES["INSTRUMENT_FAILED"] == m.facet_index.EXIT_RUNTIME, (
        "the two must stay distinct; collapsing them is what made a LIGHT "
        "install look like a broken tool")


@pytest.mark.parametrize("mod", ["numpy", "scipy", "trimesh", "PIL", "open3d"])
def test_t63_a_child_traceback_yields_its_missing_module(measure_mcp, mod):
    tb = ("Traceback (most recent call last):\n"
          "  File \"x.py\", line 1, in <module>\n"
          "    import %s\n"
          "ModuleNotFoundError: No module named '%s'\n" % (mod, mod))
    assert measure_mcp._missing_module(tb) == mod


def test_t63_the_missing_module_reader_can_miss(measure_mcp):
    """Can-fail leg: an ordinary instrument failure must NOT be reported as a
    missing dependency, or a real defect gets an install hint and is ignored."""
    assert measure_mcp._missing_module(
        "ValueError: mesh has no faces\n") is None
    assert measure_mcp._missing_module("") is None


def test_t63_a_light_module_hint_names_the_extra(measure_mcp):
    hint = measure_mcp._install_hint("numpy")
    assert "facet-mcp[measure]" in hint


def test_t63_the_open3d_hint_is_true_on_the_interpreter_it_runs_on(
        measure_mcp):
    """⚑ REWRITTEN 2026-08-09 with the ruling it enforces.

    This asserted the hint must NEVER name `measure-full`, on the reading that
    such an extra "cannot exist". Corrected: it exists and carries open3d
    behind `python_version < "3.13"`, because open3d publishes cp38-cp312 on
    PyPI and E31 measured that tier at 0 of 8 failing on py3.12.

    So the hint is now INTERPRETER-DEPENDENT, and each branch has to be true
    where it fires: on <=3.12 there IS something to install and the hint must
    say what; on 3.13 there is not, and it must say WHY rather than send the
    caller round a loop. A single fixed string cannot be honest on both.
    """
    import sys
    hint = measure_mcp._install_hint("open3d")
    assert "open3d" in hint

    if sys.version_info < (3, 13):
        assert "measure-full" in hint, (
            "on %d.%d open3d IS installable and the hint must name the extra: "
            "%r" % (sys.version_info[0], sys.version_info[1], hint))
    else:
        assert "sdist" in hint, (
            "on 3.13 there is nothing to install; the hint must say why "
            "rather than name an extra that will not deliver it: %r" % hint)
        assert "3.13" in hint, (
            "the hint should name the interpreter it is refusing on: %r" % hint)
