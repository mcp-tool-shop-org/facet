"""T47 - texel_provenance's largest connected component (E28 task 3).

E27 Ruling 7 put this IN THE INSTRUMENT, not the wrapper: a component census
computed in the server would be the measurement arithmetic gate 3 forbids. So
these legs drive the SERVED surface and read numbers the instrument printed.

The committed fixture (tests/fixtures/make_measure_fixture.py) makes the three
anchors analytic rather than tuned:

  TWINS     the styled u < 0.5 half - a solid 32x16 block, ONE 4-connected
            component, so 512 of 512.
  BRUSH s1  the edge-distance guard's interior, one region: 352 of 352.
  DILATION  160 texels in TWO components of 80. This one was PREDICTED as a
            single connected rim (E28-task3-predictions.md P19b, band 120-160)
            and measured at 80 - the unclaimed set is two disjoint bands, not a
            ring. It is kept as the anchor it is, with the miss on the record,
            and it is the most useful of the three: it is the only class in the
            fixture where the total and the component disagree, which is what
            makes the parse-independence leg below able to fail at all.

The can-fail leg is the two-thresholds law itself: a stripe variant with the
SAME TWINS total and a 16x smaller largest component. A count-only census
cannot tell those two atlases apart, which is the whole reason this measurement
was commissioned.
"""
import os
import shutil

import numpy as np
import pytest
from PIL import Image

from measure_support import PREP, STATE, call, payload


@pytest.fixture()
def scratch_state(tmp_path):
    """The committed fixture is never handed to a tool that has a writing
    path (T38's rule, carried)."""
    dst = tmp_path / "state"
    shutil.copytree(STATE, str(dst))
    return str(dst)


def _args(state):
    return {"prep": PREP, "state": state,
            "stage1": os.path.join(state, "stage1.png"),
            "order": "y+090_e+00"}


def _stripe(state):
    """Rewrite the scratch state's stage 1 into 16 alternating full-height
    columns, with the hole map as its EXACT complement so styled and holes
    stay disjoint and TWINS keeps its 512 whatever the brush then claims."""
    sm = np.zeros((32, 32), dtype=bool)
    sm[:, ::2] = True
    assert int(sm.sum()) == 512, "the variant must hold the total fixed"
    np.save(os.path.join(state, "stage1_styled_mask.npy"), sm)
    Image.fromarray(((~sm) * 255).astype(np.uint8)).save(
        os.path.join(state, "stage1_holes.png"))


def test_t47_fixture_component_anchors(scratch_state):
    c = payload(call("texel_provenance", _args(scratch_state)))["census"]
    assert c["twins"] == 512 and c["twins_largest_component"] == 512, (
        "the styled half is one solid block; its component IS its total")
    assert c["strokes"][0]["texels"] == 352
    assert c["strokes"][0]["largest_component"] == 352
    assert c["dilation"] == 160 and c["dilation_largest_component"] == 80


def test_t47_a_component_never_exceeds_its_own_class(scratch_state):
    c = payload(call("texel_provenance", _args(scratch_state)))["census"]
    pairs = [("twins", c["twins"], c["twins_largest_component"]),
             ("dilation", c["dilation"], c["dilation_largest_component"])]
    pairs += [("stroke %d" % s["stroke"], s["texels"], s["largest_component"])
              for s in c["strokes"]]
    for name, total, lcc in pairs:
        assert lcc is not None, "%s reported no component" % name
        assert 0 <= lcc <= total, (
            "%s: a subset cannot outnumber its set (%d of %d)"
            % (name, lcc, total))
        assert (lcc > 0) == (total > 0), (
            "%s: a non-empty class has a largest component and an empty one "
            "does not" % name)


def test_t47_equal_totals_separate_by_component(scratch_state):
    """THE CAN-FAIL LEG. Same TWINS total, 16x apart on the component - the
    measurement a count-only census cannot make."""
    blob = payload(call("texel_provenance",
                        _args(scratch_state)))["census"]
    _stripe(scratch_state)
    scatter = payload(call("texel_provenance",
                           _args(scratch_state)))["census"]
    assert blob["twins"] == scatter["twins"] == 512, (
        "the variant changed the total, so the pair no longer isolates shape")
    assert blob["twins_largest_component"] == 512
    assert scatter["twins_largest_component"] == 32, (
        "16 full-height columns are 16 components of 32 under 4-connectivity")
    assert (blob["twins_largest_component"]
            / scatter["twins_largest_component"]) == 16


def test_t47_the_declared_connectivity_is_four_not_eight(scratch_state):
    """ADDED AFTER A FALSIFICATION RUN, and the run is why it exists.

    Patching the instrument from `label(m2)` to 8-connectivity left all six
    other legs GREEN: the fixture's two DILATION bands do not touch even
    diagonally, and the stripe variant's columns sit two apart. So the
    instrument declared 4-connectivity in its print block, its docstring and
    the served notes, and nothing could have caught that declaration going
    false. A declaration no check can falsify is prose.

    A main-diagonal styled mask is the discriminator: 32 texels that are
    pairwise diagonal neighbours and nothing else. Under 4-connectivity they
    are 32 components of one; under 8-connectivity they are one component of
    32. The total is identical either way, which is the point.
    """
    sm = np.zeros((32, 32), dtype=bool)
    sm[np.arange(32), np.arange(32)] = True
    np.save(os.path.join(scratch_state, "stage1_styled_mask.npy"), sm)
    Image.fromarray(((~sm) * 255).astype(np.uint8)).save(
        os.path.join(scratch_state, "stage1_holes.png"))
    c = payload(call("texel_provenance", _args(scratch_state)))["census"]
    assert c["twins"] == 32
    assert c["twins_largest_component"] == 1, (
        "a diagonal chain is 32 separate components under the declared "
        "4-connectivity; 32 here would mean the instrument switched to 8")


def test_t47_the_two_blocks_are_parsed_independently(scratch_state):
    """The instrument prints the census and the component block with the same
    class labels; the component lines carry `lcc ` BEFORE the label, which is
    what keeps the four census patterns from matching them. DILATION is the
    one fixture class whose two numbers differ (160 against 80), so a pattern
    that crossed would show up here and nowhere else."""
    c = payload(call("texel_provenance", _args(scratch_state)))["census"]
    assert c["dilation"] == 160, "the total must survive the second block"
    assert c["dilation_largest_component"] == 80
    assert c["dilation"] != c["dilation_largest_component"]
    assert c["valid_texels"] == 1024, (
        "the header line is neither of the two per-class blocks")


def test_t47_the_gap_note_is_replaced_by_the_caveat(scratch_state):
    """E27 Ruling 7: the wrapper's gap-text is removed in the SAME commit that
    fills it. A gap named after it is filled is a stale claim."""
    notes = payload(call("texel_provenance",
                         _args(scratch_state)))["measure"]["notes"]
    body = " ".join(notes)
    assert not any("is NOT measured" in n for n in notes), (
        "the gap note outlived the gap")
    assert "ATLAS ADJACENCY IS NOT SURFACE ADJACENCY" in body
    assert "LOWER BOUND" in body, (
        "the direction of the bound is the caveat; without it the number "
        "reads as an exact largest region")


def test_t47_the_ratio_names_the_class_as_the_denominator(scratch_state):
    """This repo's oldest lesson. The component's denominator is its OWN
    class, not valid_texels - one region versus speckle is a within-class
    question, and normalising it by the atlas would answer a different one."""
    r = payload(call("texel_provenance",
                     _args(scratch_state)))["measure"]["ratios"]
    key = "*_largest_component"
    assert key in r, "the new pair must declare its numerator and denominator"
    assert "THAT CLASS" in r[key]["denominator"]
    assert "valid_texels" in r["census.*"]["denominator"], (
        "the census's own denominator is unchanged by this addition")
