"""T64 (E32) - the plate-geometry instrument's classifier, and the shared background fit.

WHY ITS LEGS ARE SHAPED AS FAILURES. `e32_plate_geometry.py` produces the numbers E32's
P1 and P3 are graded against - the opening count and the thinnest member's width - so a
number from an unfalsified classifier is not a measurement. This repo has caught two checks
that could not fail (a silhouette IoU returning 1.00000 on a holed mesh, a dilation
comparison returning 0.00% by construction), so every leg below is shown FAILING on
synthetic input built to fail it rather than merely agreeing with the plate as it happens
to look.

FOUR PROPERTIES, each with the wrong-implementation it discriminates against named:

  1. THE BACKGROUND FIT IS THE ROUTE'S. `mask_geometry.fit_background` must be
     bit-identical to `project_twins.fit_background`. project_twins cannot be imported
     (`ap.parse_args` at module level, line 220), so its body is extracted from source with
     `ast` and exec'd in isolation. Discriminates against: the two copies drifting apart,
     which is the failure the extraction exists to prevent and which nothing else watches.
  2. NO EROSION. A 2 px member must survive keying intact. Discriminates against:
     re-introducing `figure_mask`'s `minimum_filter(size=5)`, which deletes 2 px from every
     side and would annihilate the very structure this tool exists to measure.
  3. OPENINGS ARE ENCLOSED HOLES. An annulus has one; a C-shape whose gap reaches the
     border has none. Discriminates against: counting all background components (which
     scores both at 2) and against 8-connectivity on the background (which lets a diagonal
     1 px barrier leak, scoring a sealed diagonal cell 0).
  4. WIDTH IS A DIAMETER. A bar of KNOWN width w must read w, not w/2. Discriminates
     against: reporting the inscribed-disc radius in a field a prediction reads as a width,
     which is a factor-of-two error in the operand. Asserting `width == 2 * half_width`
     alone would be a tautology of the implementation and is deliberately not the leg.

The gradient leg is the one that would have caught a corner median: the fixture's true
background span is known by construction, and a single-sample estimator reports 0.

Source is ASCII bytes (the repo's law).
"""
import ast
import io
import json
import os
import subprocess
import sys

import numpy as np
import pytest
from PIL import Image

from conftest import REPO, tool

TOOLS = os.path.join(str(REPO), "tools")
sys.path.insert(0, TOOLS)

import mask_geometry as MG  # noqa: E402

sys.path.insert(0, os.path.join(TOOLS, "diagnostics"))
import e32_plate_geometry as PG  # noqa: E402


# ---------------------------------------------------------------------------
# 1. the shared background fit IS project_twins', proven against its own source
# ---------------------------------------------------------------------------

def _project_twins_fit_background():
    """project_twins' own body, extracted and exec'd without importing the module.

    The module builds and PARSES an argparse at import (line 220), so `import
    project_twins` cannot succeed under pytest's argv. Lifting the single function
    out with `ast` is the only way to compare against the real thing rather than
    against a second transcription of it - a transcription would make this leg a
    check of my own typing.
    """
    src = io.open(os.path.join(TOOLS, "project_twins.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    fn = [n for n in tree.body
          if isinstance(n, ast.FunctionDef) and n.name == "fit_background"]
    assert len(fn) == 1, "project_twins.fit_background not found exactly once"
    mod = ast.Module(body=fn, type_ignores=[])
    ns = {"np": np}
    exec(compile(ast.fix_missing_locations(mod), "<project_twins>", "exec"), ns)
    return ns["fit_background"]


def test_t64_shared_fit_background_is_bit_identical_to_project_twins():
    theirs = _project_twins_fit_background()
    rng = np.random.default_rng(4242)
    for shape in [(64, 48), (97, 61)]:
        img = rng.random(shape + (3,), dtype=np.float32)
        a, b = MG.fit_background(img), theirs(img)
        assert a.dtype == b.dtype == np.float64
        assert np.array_equal(a, b), "the two copies have drifted apart"


def test_t64_the_extraction_can_actually_fail():
    """The leg above is worthless if any two quadratic fits agree. A fit over a
    DIFFERENT ring width must disagree, or leg 1 cannot detect drift."""
    theirs = _project_twins_fit_background()
    img = np.random.default_rng(7).random((64, 64, 3), dtype=np.float32)
    assert not np.array_equal(MG.fit_background(img, b=8), theirs(img, b=24))


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------

def _plate(tmp_path, subject, top=90, bottom=150, name="p.png", alpha=None):
    """A plate with a KNOWN vertical background gradient and a KNOWN subject mask."""
    h, w = subject.shape
    ramp = np.linspace(top, bottom, h, dtype=np.float32)[:, None]
    img = np.repeat(ramp, w, axis=1)
    img = np.stack([img] * 3, axis=-1)
    img[subject] = 230.0
    arr = img.astype(np.uint8)
    if alpha is not None:
        arr = np.dstack([arr, alpha.astype(np.uint8)])
    p = tmp_path / name
    Image.fromarray(arr, "RGBA" if alpha is not None else "RGB").save(str(p))
    return str(p)


def _row(facts, tol):
    return [r for r in facts["tolerance_sweep"] if r["tol"] == tol][0]


# ---------------------------------------------------------------------------
# 2. NO EROSION - a 2 px member survives
# ---------------------------------------------------------------------------

def test_t64_a_two_pixel_member_survives_keying(tmp_path):
    m = np.zeros((128, 128), dtype=bool)
    m[20:100, 60:62] = True                      # a 2 px vertical tube, 80 px long
    facts = PG.measure(_plate(tmp_path, m), [0.06], 24)
    row = _row(facts, 0.06)
    assert row["area_px"] == int(m.sum()) == 160
    assert row["width_px"]["p50"] == pytest.approx(2.0, abs=1.0)


def test_t64_an_eroded_mask_would_lose_that_member():
    """The discriminating case for leg 2, made explicit: figure_mask's own
    minimum_filter(size=5) applied to the same 2 px member leaves NOTHING. If the
    tool ever adopts that erosion, the assertion above goes from 160 px to 0."""
    from scipy.ndimage import minimum_filter
    m = np.zeros((128, 128), dtype=bool)
    m[20:100, 60:62] = True
    assert minimum_filter(m.astype(np.float32), size=5).sum() == 0.0


# ---------------------------------------------------------------------------
# 3. openings are ENCLOSED holes, at the right connectivity
# ---------------------------------------------------------------------------

def _ring(n=64, r_out=26, r_in=16):
    yy, xx = np.mgrid[0:n, 0:n]
    d = np.hypot(yy - n // 2, xx - n // 2)
    return (d <= r_out) & (d >= r_in)


def test_t64_an_annulus_has_exactly_one_opening():
    assert len([a for a in PG.openings(_ring()) if a >= 16]) == 1


def test_t64_a_c_shape_has_none_because_its_gap_reaches_the_border():
    """The leg that fails a naive count-all-background-components implementation:
    that one scores the annulus 2 and this 2, and so cannot tell them apart."""
    m = _ring()
    m[:, 30:34] = False                          # cut a channel out to the frame edge
    assert [a for a in PG.openings(m) if a >= 16] == []


def test_t64_a_diagonal_one_pixel_barrier_seals_a_cell():
    """8-connectivity on the background would leak through a 1 px diagonal and score
    this 1 instead of 2. A lattice is exactly this case, repeated.

    The chord must run WALL TO WALL or it seals nothing - the first draft of this
    fixture drew a chord with both ends in open space, passed nothing, and was
    itself the check that could not fail."""
    m = np.zeros((40, 40), dtype=bool)
    m[5:35, 5] = m[5:35, 34] = m[5, 5:35] = m[34, 5:35] = True
    for i in range(15):                          # (5,20) on the top wall -> (20,5) on the left
        m[5 + i, 20 - i] = True
    areas = PG.openings(m)
    assert len(areas) >= 2, "the diagonal did not separate the cell: %r" % (areas,)


def test_t64_the_opening_curve_is_monotonic(tmp_path):
    m = _ring()
    # A 4 px pinhole punched through the ring's MATERIAL at radius ~21 - not through
    # the central void, where it would change nothing and leave the curve flat.
    m[52:54, 31:33] = False
    # ring=4, not the 24 default: on a 64 px frame a 24 px border ring reaches the
    # annulus itself, so the fit lands partly ON the subject and the key breaks. That
    # is the tool behaving correctly on a fixture too small for the flag, not a defect.
    facts = PG.measure(_plate(tmp_path, m), [0.06], 4)
    cur = _row(facts, 0.06)["openings"]
    vals = [cur["min_area_%d" % a] for a in PG.MIN_AREAS]
    assert vals == sorted(vals, reverse=True)
    assert vals[0] > vals[-1], "the curve is flat: it cannot separate speckle from a gap"


# ---------------------------------------------------------------------------
# 4. width is a DIAMETER, checked against a known width
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("w", [3, 9, 21])
def test_t64_a_bar_of_known_width_reads_that_width(tmp_path, w):
    m = np.zeros((160, 160), dtype=bool)
    m[30:130, 70:70 + w] = True
    facts = PG.measure(_plate(tmp_path, m), [0.06], 24)
    row = _row(facts, 0.06)
    # local_thickness is integer-quantised and overestimates (T25 measures
    # R = ceil(W/2)), so the diameter lands within 1 px above the true width.
    assert row["width_px"]["p50"] == pytest.approx(w, abs=1.0), row["width_px"]
    assert row["half_width_px"]["p50"] < row["width_px"]["p50"]


# ---------------------------------------------------------------------------
# 5. the gradient the corner median cannot see
# ---------------------------------------------------------------------------

def test_t64_the_fitted_background_recovers_a_known_gradient(tmp_path):
    m = np.zeros((200, 200), dtype=bool)
    m[60:140, 90:110] = True
    facts = PG.measure(_plate(tmp_path, m, top=90, bottom=150), [0.06], 24)
    luma = facts["background_fit"]["channels"]["luma"]
    assert luma["span"] == pytest.approx(60.0, abs=3.0), luma
    assert luma["bottom_row_mean"] > luma["top_row_mean"] + 50
    # and the subject is still found, which a flat-field model gets wrong
    assert _row(facts, 0.06)["area_px"] == pytest.approx(m.sum(), rel=0.05)


def test_t64_bbox_blowout_fires_when_the_subject_fills_the_frame(tmp_path):
    """The E08-registration check: a figure 751 px wide in a 752 px frame is a broken
    key, not a big subject.

    The ring must stay background or the fit lands ON the subject and the residual
    collapses - which is what the first draft of this fixture did, reporting a 4 px
    bbox for an all-figure frame. So: a 2 px rim, and a ring narrow enough to sit in
    it, giving 396/400 = 0.99 of the frame."""
    m = np.zeros((400, 400), dtype=bool)
    m[2:398, 2:398] = True
    facts = PG.measure(_plate(tmp_path, m), [0.06], 2)
    row = _row(facts, 0.06)
    assert row["bbox_frac_of_frame_w"] >= 0.98, row["bbox_wh"]
    assert row["bbox_blowout"] is True


def test_t64_bbox_blowout_is_silent_on_an_ordinary_subject(tmp_path):
    m = np.zeros((200, 200), dtype=bool)
    m[60:140, 90:110] = True
    facts = PG.measure(_plate(tmp_path, m), [0.06], 24)
    assert _row(facts, 0.06)["bbox_blowout"] is False


def test_t64_bbox_blowout_fires_on_width_alone(tmp_path):
    """E08's own case blew out in ONE dimension - 751 px wide in a 752 px frame. The
    first draft of this flag required BOTH, and stayed silent on E32's plate at
    2048/2048 wide by 1673/2048 tall, which is the exact reading it existed to catch.
    A conjunction here is governed by the clause nobody needed."""
    m = np.zeros((400, 400), dtype=bool)
    m[180:220, 2:398] = True                     # full width, 10% of the height
    facts = PG.measure(_plate(tmp_path, m), [0.06], 2)
    row = _row(facts, 0.06)
    assert row["bbox_frac_of_frame_w"] >= 0.98
    assert row["bbox_frac_of_frame_h"] < 0.5     # the clause a conjunction would fail on
    assert row["bbox_blowout"] is True
    assert row["bbox_blowout_axes"] == ["w"]


# ---------------------------------------------------------------------------
# 5b. polarity - a dark ground is excluded by construction, not by threshold
# ---------------------------------------------------------------------------

def _plate_with_dark_band(tmp_path, subject, hard=True, name="band.png"):
    """E32's plate class in miniature: a light subject, a mid grey field, and a dark
    ground across the bottom third. `hard` gives it a step edge (which no quadratic can
    fit); otherwise it ramps (which one can)."""
    h, w = subject.shape
    img = np.full((h, w, 3), 140.0, dtype=np.float32)
    cut = int(h * 0.66)
    if hard:
        img[cut:] = 40.0
    else:
        img[cut:] = np.linspace(140.0, 40.0, h - cut,
                                dtype=np.float32)[:, None, None]
    img[subject] = 230.0
    p = tmp_path / name
    Image.fromarray(img.astype(np.uint8), "RGB").save(str(p))
    return str(p)


def test_t64_a_two_sided_key_swallows_a_dark_ground(tmp_path):
    """The failure this flag exists for, asserted rather than described: at the default
    polarity the dark band IS the keyed subject, and every width read off it is wrong."""
    m = np.zeros((300, 300), dtype=bool)
    m[40:120, 145:155] = True                    # a 10 px member, 80 px long
    facts = PG.measure(_plate_with_dark_band(tmp_path, m), [0.06], 8, "both")
    row = _row(facts, 0.06)
    assert row["area_px"] > 20 * int(m.sum()), "the band was not swallowed; fixture is wrong"
    assert row["bbox_blowout"] is True
    assert row["width_px"]["p50"] > 50           # the band's width, not the member's


def test_t64_polarity_lighter_recovers_a_member_on_a_representable_ground(tmp_path):
    """What the flag is honestly for: a background the quadratic CAN represent - a smooth
    full-frame ramp - where `lighter` costs nothing and buys immunity to a dark region."""
    m = np.zeros((300, 300), dtype=bool)
    m[40:120, 145:155] = True
    facts = PG.measure(_plate(tmp_path, m, top=60, bottom=170), [0.06], 24, "lighter")
    row = _row(facts, 0.06)
    assert row["area_px"] == pytest.approx(int(m.sum()), rel=0.05), row["area_px"]
    assert row["bbox_blowout"] is False
    assert row["width_px"]["p50"] == pytest.approx(10, abs=1.0), row["width_px"]


def test_t64_polarity_lighter_does_NOT_rescue_a_hard_edged_ground(tmp_path):
    """The boundary, asserted rather than assumed. A step edge drags the ring fit down,
    so the flat upper field sits ABOVE the fitted surface and keys as subject even at
    `lighter`: 11,428 px against a true 800. Polarity selects a side; it does not make a
    quadratic fit a discontinuity. This is why E32's load-bearing plate mask comes from
    `--mask` (the route's own segmenter) and not from any key in this tool."""
    m = np.zeros((300, 300), dtype=bool)
    m[40:120, 145:155] = True
    facts = PG.measure(_plate_with_dark_band(tmp_path, m, hard=True), [0.06], 8,
                       "lighter")
    assert _row(facts, 0.06)["area_px"] > 5 * int(m.sum())


def test_t64_a_supplied_mask_bypasses_the_key_entirely(tmp_path):
    """The escape hatch that makes the paragraph above survivable: given a mask, every
    derived quantity is computed from it and no background model is consulted. Asserted
    on the plate the key demonstrably fails - if the key were still in the path, this
    would read 11,428 like the leg above."""
    m = np.zeros((300, 300), dtype=bool)
    m[40:120, 145:155] = True
    mp = tmp_path / "mask.png"
    Image.fromarray((m * 255).astype(np.uint8), "L").save(str(mp))
    facts = PG.measure(_plate_with_dark_band(tmp_path, m, hard=True, name="h.png"),
                       [0.06], 8, "lighter", str(mp))
    row = _row(facts, 0.06)
    assert facts["mask_source"] == str(mp)
    assert row["area_px"] == int(m.sum()) == 800
    assert row["width_px"]["p50"] == pytest.approx(10, abs=1.0)
    assert row["bbox_wh"] == [10, 80]


def test_t64_polarity_darker_is_the_complement_and_finds_the_band(tmp_path):
    """Proves `lighter` is selecting a side rather than merely keying less: the same
    plate at `darker` returns the band and none of the member."""
    m = np.zeros((300, 300), dtype=bool)
    m[40:120, 145:155] = True
    facts = PG.measure(_plate_with_dark_band(tmp_path, m), [0.06], 8, "darker")
    row = _row(facts, 0.06)
    assert row["area_px"] > 20 * int(m.sum())
    assert row["bbox_xyxy"][1] > 150             # the band, low in the frame


# ---------------------------------------------------------------------------
# 6. alpha: present is not the same as non-trivial
# ---------------------------------------------------------------------------

def test_t64_a_constant_255_alpha_is_present_but_not_non_trivial(tmp_path):
    m = np.zeros((64, 64), dtype=bool)
    m[20:40, 20:40] = True
    a = np.full((64, 64), 255, dtype=np.uint8)
    facts = PG.measure(_plate(tmp_path, m, alpha=a, name="opaque.png"), [0.06], 24)
    assert facts["alpha"]["channel_present"] is True
    assert facts["alpha"]["non_trivial"] is False


def test_t64_a_real_alpha_is_both(tmp_path):
    m = np.zeros((64, 64), dtype=bool)
    m[20:40, 20:40] = True
    a = np.full((64, 64), 255, dtype=np.uint8)
    a[:10, :] = 0
    facts = PG.measure(_plate(tmp_path, m, alpha=a, name="cut.png"), [0.06], 24)
    assert facts["alpha"]["channel_present"] is True
    assert facts["alpha"]["non_trivial"] is True


def test_t64_no_alpha_channel_reports_neither(tmp_path):
    m = np.zeros((64, 64), dtype=bool)
    m[20:40, 20:40] = True
    facts = PG.measure(_plate(tmp_path, m), [0.06], 24)
    assert facts["alpha"]["channel_present"] is False
    assert facts["alpha"]["non_trivial"] is False


# ---------------------------------------------------------------------------
# 7. the CLI runs, and its gates survive -O (E21 Ruling 2 / E22)
# ---------------------------------------------------------------------------

def test_t64_the_cli_writes_the_json_it_prints(tmp_path):
    m = np.zeros((96, 96), dtype=bool)
    m[30:70, 40:50] = True
    img = _plate(tmp_path, m)
    out = tmp_path / "sub" / "facts.json"      # a directory the tool must create
    r = subprocess.run([sys.executable, tool("diagnostics/e32_plate_geometry.py"),
                        "--image", img, "--tols", "0.06", "--out", str(out)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert out.exists()
    with io.open(str(out), encoding="ascii") as fh:
        assert json.load(fh)["tolerance_sweep"][0]["area_px"] > 0
