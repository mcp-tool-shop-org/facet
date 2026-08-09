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


def test_t59_the_measurement_server_is_not_in_the_wheel_today():
    """LAYER 0, pinned. `pip install facet-mcp` today gives a record server and
    no measurement server: the eight tools fail before any resolver is reached.

    This is a fact about the current tree, not a preference. When a ruling
    ships the module, this test fails and must be rewritten in that commit -
    which is how the count surfaces and the census are kept honest too.
    """
    assert "measure_mcp" not in py_modules(), (
        "measure_mcp now ships; layer 0 is closed and this file's claims "
        "about it are stale - rewrite them in the commit that ships it")
    assert not packages(), (
        "pyproject now declares packages %r; the instruments' packaging is a "
        "shape choice with a second-order cost (two generic top-level import "
        "names) and this file states the pre-choice state" % (packages(),))


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

    assert got["repo"] == str(tmp_path), (
        "the resolver did not take dirname(HERE): %r" % got["repo"])
    assert got["exists"] is False, (
        "the instrument path resolved to something that exists - this leg "
        "measures nothing: %r" % got["tool_path"])
    assert not got["tool_path"].startswith(str(site)), (
        "the named path lies INSIDE the install root, which would be layer 2 "
        "(a missing file), not layer 1 (the resolver): %r" % got["tool_path"])


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
