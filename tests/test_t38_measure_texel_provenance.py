"""T38 - texel_provenance wrapped: the census, the write-free census path,
and the sealed-tree gate on the one path that writes.

The fixture state (tests/fixtures/make_measure_fixture.py) styles the u < 0.5
half of a 32x32 atlas at stage 1 and leaves the other half holes, so TWINS is
exactly 512 and TWINS + BRUSH + DILATION is exactly 1024 whatever the brush
claims. The stroke's own claim depends on the edge-distance guard's geometry:
352 texels, pinned as an anchor when the fixture was built - if numpy or
open3d move it, this fails visibly and the fixture is re-anchored on purpose,
with the invariants beside it still holding unconditionally.
"""
import os
import shutil

import pytest

from measure_support import PREP, STATE, call, payload, refusal


@pytest.fixture()
def scratch_state(tmp_path):
    """The state, copied - the committed fixture is never handed to a tool
    that has a writing path."""
    dst = tmp_path / "state"
    shutil.copytree(STATE, str(dst))
    return str(dst)


def _args(state):
    return {"prep": PREP, "state": state,
            "stage1": os.path.join(state, "stage1.png"),
            "order": "y+090_e+00"}


def test_t38_census_counts_and_their_sum(scratch_state):
    doc = payload(call("texel_provenance", _args(scratch_state)))
    c = doc["census"]
    assert c["valid_texels"] == 1024
    assert c["twins"] == 512, "TWINS is the styled mask's own count, exact"
    assert c["strokes"][0]["key"] == "y+090_e+00"
    # the anchor: 352 at fixture creation (edge-distance 4 against the 8 px
    # painted border, minimum_filter 5). The INVARIANT rides beside it.
    assert c["strokes"][0]["texels"] == 352
    assert c["dilation"] == 160
    total = c["twins"] + sum(s["texels"] for s in c["strokes"]) + c["dilation"]
    assert total == c["valid_texels"], (
        "every texel has exactly one provenance; a census that does not sum "
        "is measuring something else")


def test_t38_census_path_writes_nothing_into_the_state(scratch_state):
    before = sorted(os.listdir(scratch_state))
    payload(call("texel_provenance", _args(scratch_state)))
    after = sorted(os.listdir(scratch_state))
    assert before == after, (
        "the census path is write-free (claim.npy belongs to --render only); "
        "new files: %s" % sorted(set(after) - set(before)))


def test_t38_render_path_refuses_inside_the_sealed_trees(
        scratch_state, monkeypatch):
    # simulate the recorded root ON the scratch copy: point FACET_ASSETS at
    # its parent, then ask for the writing path. The refusal must fire BEFORE
    # anything runs.
    monkeypatch.setenv("FACET_ASSETS", os.path.dirname(scratch_state))
    args = _args(scratch_state)
    args["render"] = os.path.join(scratch_state, "stage1.png")
    err = refusal(call("texel_provenance", args))
    assert err["code"] == "SEALED_TREE"
    assert err["exit_code"] == 4
    assert "claim.npy" in err["message"], (
        "the refusal must name WHAT would be written")
    assert sorted(os.listdir(scratch_state)) == sorted(os.listdir(scratch_state))


def test_t38_missing_job_member_refuses_naming_it(scratch_state):
    os.remove(os.path.join(scratch_state, "job_y+090_e+00", "cam.json"))
    err = refusal(call("texel_provenance", _args(scratch_state)))
    assert err["code"] == "PRECONDITION_MISSING"
    assert "cam.json" in err["message"]


def test_t38_the_census_carries_the_component_beside_every_total(scratch_state):
    """MOVED DELIBERATELY at E28 task 3, in the commit that filled the gap.

    This leg used to assert the payload NAMED the missing largest-component
    measurement (E27 Ruling 7's disclosure pattern). The instrument now makes
    that measurement, so asserting the disclaimer would pin a stale claim -
    the pin moves in the direction of demanding the number rather than
    demanding an apology for its absence. T47 owns the values and the
    two-thresholds separation; this leg owns the pairing: no total on this
    surface is reported without its component beside it.
    """
    c = payload(call("texel_provenance", _args(scratch_state)))["census"]
    assert "twins_largest_component" in c
    assert "dilation_largest_component" in c
    for s in c["strokes"]:
        assert s.get("largest_component") is not None, (
            "stroke %d reported a total with no component" % s["stroke"])
