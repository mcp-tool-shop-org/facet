"""T59 - what an INSTALLED package can and cannot do with the measurement
server (E31 task 0 / task 1).

THE HOLE THIS FILLS. T32 pinned the installed-wheel runtime for the RECORD
server after `pip install facet-mcp` shipped four releases unable to find the
record. The measurement server has the same defect at
`measure_mcp.py:139` - `REPO = os.path.dirname(HERE)`, E24's pre-fix
expression verbatim - and no test anywhere asks about it, because the module
is not in the wheel at all. E31 measured the tiers; this file keeps the parts
that run without a network round trip.

    THE LAYERS, and the order a call meets them (E31):
      layer 0  the module is not in the package               <- TRUE TODAY
      layer 1  the resolver names a path outside the install
      layer 2  the instrument file is absent from the install
      layer 3  a third-party import is missing in the child

    Measured at E31: T0 (today's wheel) is 8 of 8 at layer 0; adding the
    module alone moves all 8 to layer 1; shipping the instruments and
    resolving beside the module moves 7 of 8 to layer 3 and lets ONE through.

WHAT THIS FILE DOES NOT DO. It does not choose a shape. Whether the
instruments ship (and at what dependency tier) is [E31]'s ruling, not this
file's. Every leg below asserts a CURRENT, MEASURED state, so the commit that
adopts a shape must edit this file on purpose - which is the point.

The geometry legs use T32's transplant trick: `measure_mcp.py` in a directory
whose parent is not the record is the wheel install's defining property, and
reproducing it costs a file copy instead of a wheel, a venv and a network
round trip.

Everything printed here is ASCII (the repo's law).
"""
import json
import os
import re
import shutil
import subprocess
import sys

import pytest

from conftest import REPO, TOOLS

PYPROJECT = REPO / "pyproject.toml"
WRAPPED_REL = "verify/mesh_stats.py"


def py_modules():
    """The modules pyproject ships, read from the file every call."""
    import tomllib
    with open(str(PYPROJECT), "rb") as fh:
        doc = tomllib.load(fh)
    return doc.get("tool", {}).get("setuptools", {}).get("py-modules", [])


def packages():
    import tomllib
    with open(str(PYPROJECT), "rb") as fh:
        doc = tomllib.load(fh)
    return doc.get("tool", {}).get("setuptools", {}).get("packages", [])


# ---------------------------------------------------------------------------
# what the package ships - the can-fail leg first
# ---------------------------------------------------------------------------

def test_t59_the_pyproject_reader_can_miss():
    """THE CAN-FAIL LEG. A reader that returns [] for everything would make
    every assertion below pass on any tree."""
    mods = py_modules()
    assert "facet_index" in mods, (
        "the reader cannot see a module the wheel has shipped since v0.1.0 - "
        "it is not reading pyproject.toml")
    assert "there_is_no_such_module" not in mods


def test_t59_layer_0_is_closed_the_measurement_server_ships():
    """⚑ REWRITTEN 2026-08-09 in the commit that shipped it, as this test's
    previous body instructed.

    It read `assert "measure_mcp" not in py_modules()` and said: *this is a
    fact about the current tree, not a preference; when a ruling ships the
    module, this test fails and must be rewritten in that commit.* E31 Ruling
    6 shipped it at the Director's word, so layer 0 is closed and the pin
    turns around to hold it closed.

    LAYER 0 WAS THE FAILURE IN FRONT OF ALL THE OTHERS: at tier T0 the module
    was not in the artifact at all, so "where does it fail" had no operand and
    all eight tools failed before any resolver ran. Each assertion below
    un-ships something if it is deleted.
    """
    mods = py_modules()
    assert "measure_mcp" in mods, (
        "measure_mcp left py-modules - `pip install facet-mcp` is back to a "
        "record server with no measurement server (E31 tier T0, 8 of 8)")
    assert "subject_profile" in mods, (
        "subject_profile left py-modules - mesh_stats imports it, and without "
        "it that tool fails at layer 3 in an install (E31 tier T2 -> T2b)")
    assert set(packages()) == {"diagnostics", "verify"}, (
        "the instrument directories are no longer both packaged (%r) - the "
        "served tools invoke instruments as SUBPROCESSES, so a wheel without "
        "them has nothing to invoke" % (packages(),))


def test_t59_the_light_extra_is_declared_and_open3d_is_not_in_it():
    """The tier, pinned - and the absence pinned with it.

    `[measure]` is the honest ceiling rather than a first tier with a bigger
    one behind it: open3d 0.19.0 publishes cp38-cp312 and no sdist, and the
    only cp313 build is a direct-URL dev wheel, which CANNOT appear in
    metadata uploaded to PyPI (E31 Ruling 3a). A `measure-full` extra naming
    open3d would be unsatisfiable on the interpreter this repo runs on.
    """
    import tomllib
    with open(os.path.join(REPO, "pyproject.toml"), "rb") as fh:
        extras = tomllib.load(fh)["project"].get("optional-dependencies", {})
    assert "measure" in extras, "the [measure] extra is gone"
    names = {re.split(r"[<>=!\[ ]", d, 1)[0].lower() for d in extras["measure"]}
    assert {"numpy", "scipy", "trimesh", "pillow"} <= names, (
        "the [measure] extra no longer covers the four LIGHT modules: %r"
        % (sorted(names),))
    for extra, deps in extras.items():
        flat = " ".join(deps).lower()
        assert "open3d" not in flat, (
            "extra %r names open3d - there is no PyPI-installable open3d for "
            "this package's declared Python range, so this extra cannot be "
            "satisfied (E31 Ruling 3a)" % extra)


# ---------------------------------------------------------------------------
# layer 1 - the resolver, reproduced without a wheel
# ---------------------------------------------------------------------------

def _transplant(tmp_path):
    """measure_mcp.py + facet_index.py in a directory whose parent is NOT the
    record. `facet_index` rides along because measure_mcp imports it at module
    level; nothing else is copied, which is the wheel's own shape."""
    site = tmp_path / "site-packages"
    site.mkdir()
    for name in ("facet_index.py", "measure_mcp.py"):
        shutil.copy2(str(TOOLS / name), str(site / name))
    for marker in ("CLAUDE.md", "docs"):
        assert not os.path.exists(os.path.join(str(tmp_path), marker)), (
            "the transplant's parent must not look like a checkout, or this "
            "leg measures nothing")
    return site


_PROBE = (
    "import json, os, sys\n"
    "import measure_mcp as m\n"
    "print(json.dumps({\n"
    "    'repo': m.REPO,\n"
    "    'tool_path': m.tool_path(%r),\n"
    "    'exists': os.path.exists(m.tool_path(%r)),\n"
    "}))\n" % (WRAPPED_REL, WRAPPED_REL)
)


def _probe(site, cwd):
    env = dict(os.environ)
    env["PYTHONPATH"] = str(site)
    env.pop("FACET_INDEX_DB", None)
    p = subprocess.run([sys.executable, "-c", _PROBE], cwd=str(cwd), env=env,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=300)
    assert p.returncode == 0, p.stderr
    return json.loads(p.stdout.strip().splitlines()[-1])


def test_t59_transplanted_measure_mcp_resolves_outside_its_own_install(tmp_path):
    """LAYER 1, measured. `REPO = dirname(HERE)` puts the instrument search one
    directory ABOVE the install root - `<venv>/Lib/tools/...` for a wheel whose
    modules sit in `<venv>/Lib/site-packages`. The path named is not merely
    absent; it is outside the package entirely, which is what separates a
    resolver defect from a missing file."""
    site = _transplant(tmp_path)
    got = _probe(site, tmp_path)

    # ⚑ REWRITTEN 2026-08-09 in the commit that fixed the defect it pinned.
    # It read `assert got["repo"] == str(tmp_path)` - dirname(HERE), E24's
    # defect verbatim, naming `<venv>\Lib\tools\verify\mesh_stats.py`, OUTSIDE
    # the install entirely. Both halves now behave, and they behave for two
    # DIFFERENT reasons, which is the distinction the repair turns on:
    assert got["repo"] is None, (
        "REPO is a CORPUS question and this directory holds no corpus, so the "
        "resolver must return None rather than guess - E24's constraint. Got "
        "%r" % got["repo"])
    assert got["tool_path"].startswith(str(site)), (
        "the instrument path is an INSTRUMENT question, answered beside the "
        "module, so it must land inside the install root even when no corpus "
        "exists: %r" % got["tool_path"])
    assert got["exists"] is False, (
        "this transplant deliberately copies the two modules and NOT the "
        "instrument directories, so the named file must be absent - that is "
        "layer 2 (a missing file), which packaging closes. If it exists, this "
        "leg measures nothing: %r" % got["tool_path"])


def test_t59_a_checkout_still_resolves_its_instruments(tmp_path):
    """The path that works must keep working: run from the repo, `tool_path`
    names a file that is there. Without this leg the one above could be
    satisfied by a resolver that is broken everywhere."""
    site = tmp_path / "not-used"
    site.mkdir()
    env = dict(os.environ)
    env.pop("FACET_INDEX_DB", None)
    p = subprocess.run([sys.executable, "-c", _PROBE], cwd=str(TOOLS),
                       env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=300)
    assert p.returncode == 0, p.stderr
    got = json.loads(p.stdout.strip().splitlines()[-1])
    assert got["repo"] == str(REPO)
    assert got["exists"] is True, got["tool_path"]


def test_t59_the_instrument_sits_beside_the_module_in_the_source_tree():
    """The shape a package-relative resolver would need, asserted as AVAILABLE
    rather than adopted: `tools/` holds the modules AND the two instrument
    directories, so `join(HERE, rel)` is correct in a checkout and would be
    correct in an install that shipped them beside the modules. Stating it here
    means the ruling is choosing between measured options."""
    assert (TOOLS / "measure_mcp.py").exists()
    assert (TOOLS / WRAPPED_REL.replace("/", os.sep)).exists()
    assert (TOOLS / "diagnostics").is_dir()
    assert (TOOLS / "verify").is_dir()


# ---------------------------------------------------------------------------
# the one path that survives every layer
# ---------------------------------------------------------------------------

def test_t59_measure_report_comparison_half_names_no_instrument():
    """THE RAREST CLAUSE. Seven of the eight tools reach an instrument file on
    every path; `measure_report`'s comparison half does not - it passes
    `instrument_rel=None` to `envelope`, so nothing is joined onto REPO and
    nothing is hashed. That is why it is the ONE call that returns a payload
    from an install with no instruments and no third-party dependency at all
    (E31, tiers T1 and T2).

    A change that gave this path an instrument would close the only door the
    measurement server has on a dependency-free install, and would do it
    silently. This leg is what would notice.
    """
    from measure_support import call, payload

    fake = {"n": 1, "measure": {
        "tool": "mesh_stats",
        "server": {"name": "facet-measure", "version": "x"},
        "instrument": {"path": "p", "sha256": "s"},
        "config_hash": "c"}}
    doc = payload(call("measure_report",
                       {"left": fake, "right": dict(fake, n=2)}))
    assert doc["measure"]["instrument"] is None, (
        "the comparison half now names an instrument: %r"
        % (doc["measure"]["instrument"],))
    assert doc["comparison"]["rows"]["n"]["delta"] == 1
    notes = " ".join(doc["measure"].get("notes") or [])
    assert "no instrument ran" in notes, (
        "the payload no longer states that no instrument ran")


@pytest.mark.parametrize("tier", ["sheet"])
def test_t59_measure_report_sheet_half_does_reach_an_instrument(tier):
    """The other half of the same tool, so the leg above is a distinction and
    not an accident of how measure_report happens to be called."""
    import measure_mcp

    assert measure_mcp.WRAPPED["measure_report"] == "tools/verify/gate1_sheet.py"
    assert os.path.exists(measure_mcp.tool_path("verify/gate1_sheet.py"))
