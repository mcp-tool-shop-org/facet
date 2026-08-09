"""T45 - the served offsurface_rate, at the surface (E28 2b, wrap 3 of 3).

Wraps tools/diagnostics/e12_offsurface.py - the BAKE half only; the erode /
margin-statistic half exists in NEITHER offsurface instrument and the payload
notes say so (E27 Ruling 7's pattern: name the gap, do not compute it).

The hermetic legs use the synthetic quad prep, whose position map lies ON its
mesh by construction - so the off-surface rate is analytically ZERO - and a
SHIFTED copy of the same prep, whose rate is analytically ONE HUNDRED: the
pair is the can-fail proof, because a wrap that always returned 0 passes the
first and fails the second. The anchor reproduces E12 task 2's recorded
dragon numbers digit for digit at the served surface.
"""
import io
import json
import os
import shutil

import numpy as np
import pytest

from conftest import REPO, ASSETS_ENV, DEFAULT_ASSETS
from measure_support import PREP, call, payload, refusal


# ---------------------------------------------------------------------------
# hermetic - the quad prep and its deliberately broken twin
# ---------------------------------------------------------------------------

def test_t45_the_synthetic_quad_is_on_its_own_surface():
    doc = payload(call("offsurface_rate", {"prep": PREP}))
    assert doc["uv_valid_texels"] == 1024
    assert doc["sampled"] == 1024
    assert doc["pct_off_surface_gt_1px"] == 0.0, (
        "the fixture's position map lies ON its mesh by construction; a "
        "nonzero rate here is the wrap (or the unit) inventing distance")
    assert doc["pct_off_surface_gt_5px"] == 0.0
    # NOT == 0.0: the reconstruction runs in float32 and the quad's measured
    # median is 2.980e-08 canonical (a ten-thousandth of an emit pixel) -
    # kernel residue, not distance. Asserting exact zero here failed on first
    # run and would have been this test inventing a precision the instrument
    # never claimed; the bound is a thousandth of a pixel, three orders above
    # the residue and three below the 1px class boundary.
    assert doc["median_distance_px"] < 1e-3


def test_t45_a_shifted_bake_reads_fully_off_surface(tmp_path):
    """The can-fail direction: copy the quad prep, push every reconstructed
    position 0.2 canonical units off the plane, and the rate must read 100 -
    the wrap seeing exactly the defect this tool exists to see."""
    broken = tmp_path / "prep"
    shutil.copytree(PREP, str(broken))
    with io.open(os.path.join(str(broken), "meta.json"),
                 encoding="utf-8") as fh:
        meta = json.load(fh)
    pos = np.load(os.path.join(str(broken), "pos.npy"))
    # pos is normalised into [lo, hi]; the quad is the x = 1.0 plane, so
    # shifting normalised x DOWN moves world x off the plane... unless lo == hi
    # on that axis, in which case shift a spanned axis in WORLD terms by
    # rewriting meta's lo/hi instead. Simplest robust break: move the whole
    # reconstruction off the mesh by translating lo and hi together.
    meta["lo"] = [v + 0.2 for v in meta["lo"]]
    meta["hi"] = [v + 0.2 for v in meta["hi"]]
    with io.open(os.path.join(str(broken), "meta.json"), "w",
                 encoding="utf-8") as fh:
        json.dump(meta, fh)
    np.save(os.path.join(str(broken), "pos.npy"), pos)  # unchanged, on purpose
    doc = payload(call("offsurface_rate", {"prep": str(broken)}))
    assert doc["pct_off_surface_gt_1px"] == 100.0, (
        "every reconstructed position was translated 0.2 canonical units off "
        "the quad and the rate did not read 100%% - got %r"
        % doc["pct_off_surface_gt_1px"])


def test_t45_fixed_seed_is_actually_fixed():
    a = payload(call("offsurface_rate", {"prep": PREP}))
    b = payload(call("offsurface_rate", {"prep": PREP}))
    for k in ("median_distance", "pct_off_surface_gt_1px", "max_distance_px",
              "sampled"):
        assert a[k] == b[k], "seeded sampling drifted on %s" % k


def test_t45_envelope_names_the_erode_margin_gap():
    doc = payload(call("offsurface_rate", {"prep": PREP}))
    env = doc["measure"]
    assert env["tool"] == "offsurface_rate"
    assert env["instrument"]["path"] == "tools/diagnostics/e12_offsurface.py"
    assert len(env["instrument"]["sha256"]) == 64
    assert any("ERODE" in n or "erode" in n for n in env["notes"]), (
        "the spec's erode/margin half exists in neither offsurface "
        "instrument; the payload must NAME the gap, not imply completeness")
    assert any("e10_offsurface" in n for n in env["notes"])
    assert "pct_off_surface_gt_1px" in env["ratios"]
    assert "v_ext_derivation" in doc, (
        "the emit-pixel unit's derivation travels with the number - getting "
        "it wrong scales every threshold")


def test_t45_missing_prep_member_refuses_naming_it(tmp_path):
    bare = tmp_path / "prep"
    bare.mkdir()
    err = refusal(call("offsurface_rate", {"prep": str(bare)}))
    assert err["code"] == "PRECONDITION_MISSING"
    assert "meta.json" in err["message"]


# ---------------------------------------------------------------------------
# the anchor - E12 task 2's recorded dragon numbers, defaults reproduce them
# ---------------------------------------------------------------------------

@pytest.mark.artifacts
def test_t45_served_tool_reproduces_e12s_recorded_offsurface():
    """E12-task2-report.md's validated table, dragon row: one emit px
    6.718107e-04, median distance 0.0013 px, >1 px 2.6430%, >5 px 2.4395%,
    max 377.6 px - measured with the instrument's own defaults (fixed seed 0,
    sample 200000, the subject's ruled framing), which is what this call
    passes. The ship row (2.5065% against E10 Ruling 4's ruled 2.5%) is the
    instrument's own validation anchor and stays in the record."""
    root = os.environ.get(ASSETS_ENV, DEFAULT_ASSETS)
    prep = os.path.join(root, "facet_next", "E12_prep")
    if not os.path.exists(os.path.join(prep, "meta.json")):
        pytest.skip("recorded tree absent: %s" % prep)
    doc = payload(call("offsurface_rate", {"prep": prep}))
    assert doc["uv_valid_texels"] == 3240510
    assert round(doc["one_px"], 10) == round(6.718107e-04, 10)
    assert round(doc["pct_off_surface_gt_1px"], 4) == 2.6430
    assert round(doc["pct_off_surface_gt_5px"], 4) == 2.4395
    assert round(doc["median_distance_px"], 4) == 0.0013
    assert round(doc["max_distance_px"], 1) == 377.6
