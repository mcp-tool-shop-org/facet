"""T43 - the served mesh_topology, at the surface (E28 2b, wrap 1 of 3).

The served tool wraps tools/diagnostics/e14_topology.py ALONE (E28 Ruling 4:
e12_nonmanifold.py is NAMED in the payload notes as the independent
concentration picture, never wrapped). Hermetic legs run the fixture meshes -
each one built to exhibit one defect class, so the assertions test failure
modes rather than a success mode. The anchor reproduces E14 Gate 0's recorded
longsword numbers digit for digit at the served surface, T37's pattern.
"""
import os

import pytest

from conftest import REPO, ASSETS_ENV, DEFAULT_ASSETS
from measure_support import MESHES, call, payload, refusal


def mesh(name):
    return os.path.join(MESHES, name)


# ---------------------------------------------------------------------------
# hermetic - the fixture ladder, one defect class each
# ---------------------------------------------------------------------------

def test_t43_cube_is_one_closed_clean_shell(tmp_path):
    doc = payload(call("mesh_topology", {"glb": mesh("cube.glb")}))
    assert doc["shells"] == 1
    assert doc["boundary_edges"] == 0
    assert doc["boundary_total_length"] == 0.0
    assert doc["nonmanifold_edges"] == 0
    # the tie repair at the served surface: the cube's extents are all equal,
    # the crash class E27 measured, and the scan still names three real axes
    cs = doc["cross_sections"]
    assert {cs["scan_axis"], cs["thin_axis"]} <= {"x", "y", "z"}
    assert cs["scan_axis"] != cs["thin_axis"]


def test_t43_twoshell_counts_two_vertex_shells():
    doc = payload(call("mesh_topology", {"glb": mesh("twoshell.glb")}))
    assert doc["shells"] == 2, (
        "the two-shell fixture must read 2 under the shared-vertex "
        "definition; got %r" % doc["shells"])


def test_t43_nonmanifold_fixture_reads_nonzero_where_cube_reads_zero():
    doc = payload(call("mesh_topology", {"glb": mesh("nonmanifold.glb")}))
    assert doc["nonmanifold_edges"] > 0, (
        "the pinched fixture exists to exercise exactly this counter")


def test_t43_open_sheet_carries_boundary_edges_with_length():
    doc = payload(call("mesh_topology", {"glb": mesh("sheet.glb")}))
    assert doc["boundary_edges"] > 0
    assert doc["boundary_total_length"] > 0.0, (
        "an open sheet's boundary loop has LENGTH - count without length is "
        "the degenerate-edge confusion the instrument exists to separate")


def test_t43_both_shell_definitions_ride_the_payload():
    """The instrument's operand warning, made structural: `shells` (the
    family-table quantity) and `pieces_manifold_adjacency` are different
    numbers on a pinched surface and BOTH must be present and named."""
    doc = payload(call("mesh_topology", {"glb": mesh("cube.glb")}))
    assert "shells" in doc and "pieces_manifold_adjacency" in doc
    assert "shared-vertex" in doc["shells_definition"]
    assert "MANIFOLD" in doc["pieces_definition"]


def test_t43_envelope_and_notes():
    doc = payload(call("mesh_topology", {"glb": mesh("cube.glb")}))
    env = doc["measure"]
    assert env["tool"] == "mesh_topology"
    assert env["instrument"]["path"] == "tools/diagnostics/e14_topology.py"
    assert len(env["instrument"]["sha256"]) == 64
    assert env["metrics_label"] == "diagnostic"
    assert "nonmanifold_frac" in env["ratios"]
    assert any("e12_nonmanifold" in n for n in env["notes"]), (
        "E28 Ruling 4: the independent concentration picture is NAMED in the "
        "payload notes, never wrapped")


def test_t43_missing_mesh_refuses_naming_it():
    err = refusal(call("mesh_topology", {"glb": "no-such.glb"}))
    assert err["code"] == "PRECONDITION_MISSING"
    assert "no-such.glb" in err["message"]


# ---------------------------------------------------------------------------
# the anchor - E14 Gate 0's recorded longsword numbers, at the served surface
# ---------------------------------------------------------------------------

@pytest.mark.artifacts
def test_t43_served_tool_reproduces_e14_gate0s_recorded_topology():
    """E14-gate0-report.md, the candidate table: longsword_00001 measured
    shells (welded) 1, boundary edges 0, total boundary length 0.00000000,
    non-manifold edges 121 (0.0081%). The SERVED tool must reproduce every
    digit - the wrap is proven not to change the instrument, which is the one
    thing it exists not to do (T37's pattern)."""
    root = os.environ.get(ASSETS_ENV, DEFAULT_ASSETS)
    glb = os.path.join(root, "facet_next", "E14_gate0",
                       "longsword_00001_raw.glb")
    if not os.path.exists(glb):
        pytest.skip("recorded tree absent: %s" % glb)
    doc = payload(call("mesh_topology", {"glb": glb}))
    assert doc["shells"] == 1
    assert doc["boundary_edges"] == 0
    assert doc["boundary_total_length"] == 0.0
    assert doc["nonmanifold_edges"] == 121
    assert round(100 * doc["nonmanifold_frac"], 4) == 0.0081
