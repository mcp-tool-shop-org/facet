"""T44 - the served thin_extent_curve, at the surface (E28 2b, wrap 2 of 3).

Wraps tools/diagnostics/e12_thin_curve.py. The hermetic legs pin the curve's
two analytic endpoints on the cube - value 0 withholds NOTHING (the tool
default, undecided-runs-disabled) and a value larger than the mesh withholds
EVERYTHING - so an instrument that returned a flat curve fails one of the
pair; a check that cannot fail is not a check. The anchor reproduces E12 task
2b's recorded dragon curve digit for digit at the served surface, including
the wing-region column, with the exact recorded invocation.
"""
import os

import pytest

from conftest import REPO, ASSETS_ENV, DEFAULT_ASSETS
from measure_support import MESHES, call, payload, refusal

# small grid for the hermetic legs: the instrument's arithmetic is per-pixel
# identical at any aspect, and CI does not owe 29M rays to a unit cube
FAST = {"aspect": "448,256", "views": "0,90", "values": "0,10"}


def test_t44_the_two_analytic_endpoints_of_the_curve(tmp_path):
    doc = payload(call("thin_extent_curve",
                       dict(FAST, glb=os.path.join(MESHES, "cube.glb"))))
    c = doc["curve"]
    assert c["0"]["figure_pct"] == 0.0, (
        "value 0 is the tool default - the guard DISABLED - and must withhold "
        "nothing; a nonzero here is the instrument inventing a threshold")
    assert c["10"]["figure_pct"] == 100.0, (
        "a value larger than the whole mesh must withhold every hit pixel on "
        "a closed solid; anything less means ext is not being computed")
    assert doc["total_hit_px"] > 0


def test_t44_per_view_rows_and_unit_ride_the_payload():
    doc = payload(call("thin_extent_curve",
                       dict(FAST, glb=os.path.join(MESHES, "cube.glb"))))
    assert set(doc["per_view"]) == {"0", "90"}
    assert doc["one_px"] > 0
    assert doc["h_ext"] > 0 and doc["v_ext"] > 0
    env = doc["measure"]
    assert env["tool"] == "thin_extent_curve"
    assert env["instrument"]["path"] == "tools/diagnostics/e12_thin_curve.py"
    assert len(env["instrument"]["sha256"]) == 64
    assert "curve.*.figure_pct" in env["ratios"]


def test_t44_a_lone_region_rect_refuses():
    """The wrapper's own precondition: the region is read off TWO orthogonal
    views or not at all."""
    err = refusal(call("thin_extent_curve",
                       dict(FAST, glb=os.path.join(MESHES, "cube.glb"),
                            region_a="0:1,1,10,10")))
    assert err["code"] == "BAD_ARGUMENT"
    assert "pair" in err["message"]


def test_t44_missing_mesh_refuses_naming_it():
    err = refusal(call("thin_extent_curve", {"glb": "no-such.glb"}))
    assert err["code"] == "PRECONDITION_MISSING"
    assert "no-such.glb" in err["message"]


# ---------------------------------------------------------------------------
# the anchor - E12 task 2b's recorded dragon curve, exact invocation
# ---------------------------------------------------------------------------

@pytest.mark.artifacts
def test_t44_served_tool_reproduces_e12s_recorded_curve():
    """E12-task2b-report.md: on the dragon's ruled framing one emit pixel is
    6.718107e-04 canonical units; the ship's 0.01 withholds 15.304% of the
    figure and 26.819% of the wing region; the character's 0.03 withholds
    33.863% and 60.418%. The recorded invocation is quoted at the top of that
    report and repeated here verbatim (the values list is a subset - each
    value thresholds the same extent field independently, so a subset does
    not move any row).

    THE PIN IS THE PAYLOAD'S OWN 4-DECIMAL PRECISION, one rounding earlier
    than the report's 3-decimal prints, because comparing across the two
    roundings breaks at a half boundary: the served region value is 26.8195,
    whose raw was in [26.81945, 26.8195) and printed as the recorded 26.819 -
    while round(26.8195, 3) is 26.82. The first run of this anchor failed on
    exactly that, with every value consistent with the record. Each pin below
    prints to the recorded digits: 15.3043 -> 15.304, 26.8195 -> 26.819,
    33.8626 -> 33.863, 60.418 -> 60.418, 6.7181068e-04 -> 6.718107e-04."""
    root = os.environ.get(ASSETS_ENV, DEFAULT_ASSETS)
    glb = os.path.join(root, "facet_next", "E12_prep", "prep_uv.glb")
    if not os.path.exists(glb):
        pytest.skip("recorded tree absent: %s" % glb)
    doc = payload(call("thin_extent_curve", {
        "glb": glb, "aspect": "1792,1024", "fit_axis": "width",
        "views": "0,45,90,135,180,225,270,315",
        "values": "0,0.01,0.03",
        "region_a": "0:1120,0,1791,1023", "region_b": "90:0,0,1791,1023"}))
    assert round(doc["one_px"], 10) == round(6.718107e-04, 10)
    c = doc["curve"]
    assert c["0.01"]["figure_pct"] == 15.3043
    assert c["0.01"]["region_pct"] == 26.8195
    assert c["0.03"]["figure_pct"] == 33.8626
    assert c["0.03"]["region_pct"] == 60.418
    assert c["0"]["figure_pct"] == 0.0
