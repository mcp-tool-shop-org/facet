"""T36 - mesh_stats wrapped, on meshes whose numbers are derived, not tuned.

The fixtures are constructions (tests/fixtures/make_measure_fixture.py): a
box welds to 8 vertices and 1 component but exports as 6 per-face vertex
islands; the pinch pair shares exactly one corner so the vertex census reads
1 where the manifold-edge census reads 2; the sliver's silhouette is tiny
against the default face rect so the not-a-face-readout warning MUST fire.
Every number asserted here is a property of the construction.
"""
import os

import pytest

from measure_support import MESHES, call, payload, refusal


@pytest.fixture(scope="module")
def stats():
    """One wrapped call per mesh, shared across this module's asserts."""
    out = {}
    for name in ("cube", "pinch", "twoshell", "sheet", "sliver"):
        out[name] = payload(call("mesh_stats",
                                 {"glb": os.path.join(MESHES,
                                                      name + ".glb")}))
    return out


def test_t36_cube_welds_to_one_component_from_six_islands(stats):
    m = stats["cube"]["mesh"]
    assert m["faces"] == 12 and m["verts"] == 8
    assert m["components"] == 1
    assert m["watertight"] is True
    # the weld law made visible: a GLB export splits vertices at every normal
    # discontinuity, so the unwelded box is six disconnected face-islands
    assert m["components_unwelded"] == 6
    assert m["verts_unwelded"] == 24


def test_t36_pinch_reads_one_under_the_vertex_definition(stats):
    m = stats["pinch"]["mesh"]
    # two boxes sharing exactly one corner: mesh_stats' census is components
    # joined by a SHARED VERTEX, so the pinch is ONE shell here - the manifold
    # -edge census (e14_topology's pieces column) reads 2 on this same mesh,
    # which is the disagreement the fixture exists to expose (E27 P5)
    assert m["components"] == 1
    assert m["verts"] == 15, "16 corners minus the one shared = 15"
    assert m["faces"] == 24


def test_t36_twoshell_reads_two_under_both_definitions(stats):
    m = stats["twoshell"]["mesh"]
    assert m["components"] == 2
    assert m["largest_component_frac"] == 0.5


def test_t36_sheet_is_open_and_its_empty_rect_is_null_not_nan(stats):
    m = stats["sheet"]["mesh"]
    assert m["watertight"] is False
    assert m["components"] == 1
    # no vertex lands in the face rect, so curvature is undefined there. NaN
    # is not valid strict JSON and not a number a caller can use: the wrapper
    # carries it as null and NAMES the conversion
    assert m["face_curvature_var"] is None
    named = stats["sheet"]["measure"]["nan_as_null"]
    assert any("face_curvature_var" in p for p in named), named


def test_t36_warnings_are_surfaced_not_swallowed(stats):
    w = stats["sliver"]["measure"]["warnings"]
    assert any("cannot be measuring a face" in ln for ln in w), (
        "the sliver's rect_frac warning fired on stdout and must ride the "
        "payload: %r" % w)


def test_t36_missing_mesh_refuses_naming_the_path():
    err = refusal(call("mesh_stats", {"glb": os.path.join(MESHES,
                                                          "absent.glb")}))
    assert err["code"] == "PRECONDITION_MISSING"
    assert err["exit_code"] == 4
    assert "absent.glb" in err["message"], (
        "a refusal that does not name the missing input cannot be acted on")
