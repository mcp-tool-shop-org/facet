"""T35 - the measurement server's surface and its identity envelope (E27).

Source: docs/specs/measurement-mcp-spec.md - the tool table (eight names, the
contract), the instrument-identity law (every payload carries the server
version and a hash of the measurement configuration), and the
diagnostics-are-not-gates law (every metric labelled).

The surface is tested through Client(server) - the SDK's own dispatch - plus
one spawn of the entry point, because an in-process client cannot prove
`python tools/measure_mcp.py` runs at all (T22's reasoning, inherited).
"""
import os
import re
import subprocess
import sys

from conftest import REPO, TOOLS
from measure_support import (MESHES, call, list_tools, measure_mcp, payload)

EIGHT = ("mesh_stats", "mesh_topology", "reach_ceiling", "thin_extent_curve",
         "offsurface_rate", "texel_provenance", "anchor_check",
         "measure_report")


def test_t35_the_surface_is_exactly_the_specs_eight_tools():
    tools = {t.name: t for t in list_tools().tools}
    assert set(tools) == set(EIGHT), (
        "the tool surface drifted from spec 2's table: %s"
        % sorted(set(tools) ^ set(EIGHT)))
    for name, t in tools.items():
        assert t.annotations is not None, "%s carries no annotations" % name
        assert t.annotations.read_only_hint is True, (
            "%s is not marked read-only; this server modifies no asset" % name)


def test_t35_print_tools_runs_under_the_exit_contract():
    p = subprocess.run(
        [sys.executable, str(TOOLS / "measure_mcp.py"), "--print-tools"],
        cwd=str(REPO), capture_output=True, timeout=600)
    out = p.stdout.decode("ascii", errors="replace")
    assert p.returncode == 0, out + p.stderr.decode("ascii", errors="replace")
    for name in EIGHT:
        assert name in out, "--print-tools does not list %s" % name
    # Moved deliberately at E28 2c (the pin's second move, with T40's): the
    # line used to assert the refusal marker was PRESENT, because four tools
    # refused. Since Ruling 10's eighth wrap every name serves, so the
    # printable surface must carry a real instrument per line and no refusal
    # marker anywhere.
    assert "REFUSES" not in out, (
        "--print-tools shows a refusal marker; since E28 2c all eight serve")
    assert out.count("wraps: tools/") == 8, (
        "every one of the eight lines names its instrument")


def test_t35_envelope_carries_version_instrument_hash_and_config_hash():
    doc = payload(call("mesh_stats",
                       {"glb": os.path.join(MESHES, "cube.glb")}))
    env = doc["measure"]
    assert env["server"] == {"name": "facet-measure",
                             "version": measure_mcp.MEASURE_VERSION}
    assert env["tool"] == "mesh_stats"
    inst = env["instrument"]
    assert inst["path"] == "tools/verify/mesh_stats.py"
    live = measure_mcp._sha256_file(
        os.path.join(str(REPO), "tools", "verify", "mesh_stats.py"))
    assert inst["sha256"] == live, (
        "the envelope's instrument hash is not the file on disk - identity "
        "would be decorative")
    assert re.fullmatch(r"[0-9a-f]{64}", env["config_hash"])
    assert env["metrics_label"] == "diagnostic"


def test_t35_config_hash_is_deterministic_and_parameter_sensitive():
    a = payload(call("mesh_stats",
                     {"glb": os.path.join(MESHES, "cube.glb")}))
    b = payload(call("mesh_stats",
                     {"glb": os.path.join(MESHES, "cube.glb")}))
    c = payload(call("mesh_stats",
                     {"glb": os.path.join(MESHES, "cube.glb"), "grid": 128}))
    assert a["measure"]["config_hash"] == b["measure"]["config_hash"], (
        "same tool, same params, different hash - the identity contract "
        "cannot hold")
    assert a["measure"]["config_hash"] != c["measure"]["config_hash"], (
        "a changed parameter left the config hash unchanged - a mismatch "
        "this hash cannot see is a comparison it cannot refuse")


def test_t35_every_ratio_names_numerator_and_denominator():
    doc = payload(call("mesh_stats",
                       {"glb": os.path.join(MESHES, "cube.glb")}))
    ratios = doc["measure"]["ratios"]
    assert ratios, "mesh_stats returns ratios; the payload must name them"
    for key, pair in ratios.items():
        assert pair.get("numerator"), "%s names no numerator" % key
        assert pair.get("denominator"), "%s names no denominator" % key
