"""T66 (E35) - the dark-speck detector: exact censuses on planted fixtures, ANDONs shown
FIRING, -O survival, and the R-a validation against artifacts the DIRECTOR rejected.

WHY THE VALIDATION CORPUS IS HIS REJECTS AND NOT MY FIXTURES. E07 spent four arms and two
gates on metrics that could not separate an asset he rejected from one he accepted - four of
its five numbers were 5x5 high-pass statistics blind to the defect that decides acceptance.
So the census is not adopted because its author's synthetic dots come out right; it is
adopted because it FIRES on the twins carrying the class he called unacceptable and stays
QUIET on the clay controls, which the E34-seat attribution measured at ZERO near-black px.
Those two legs are the ones E35 R-a puts in front of every A/B number.

WHY THE PLANTED LEGS ASSERT EXACT COUNTS. A detector that returns "some blobs" cannot be
distinguished from one that returns noise. Each fixture plants a known number of dots of
known area on a known register, so the expected census is arithmetic, not a range.

WHY EVERY ANDON LEG IS A FAILURE CASE WITH A COMPANION SUCCESS. This repo has caught two
checks that could not fail - a silhouette IoU returning 1.00000 on a holed mesh, and a
dilation comparison returning 0.00% by construction. A leg that only agrees with the happy
path is not evidence, so each guard is shown refusing the wrong input AND accepting the
right one.

THE ANDONs ARE `raise`, NEVER `assert`. `python -O` and PYTHONOPTIMIZE=1 delete asserts
silently, and 87 of this repo's gates were removable by an environment variable until E22
converted them (E21 Ruling 2). Leg 7 runs a firing case under -O and under PYTHONOPTIMIZE=1
and asserts it still halts.

Source is ASCII bytes (the repo's law).
"""
import json
import os
import subprocess
import sys

import numpy as np
import pytest
from PIL import Image

from conftest import assets_root, need, tool

REGISTER = (144, 102, 77)      # the performer's measured terracotta register
SPECK = (80, 50, 28)           # a measured speck core, ~23 L* below the register


def _plant(path, size=(120, 160), dots=(), register=REGISTER, speck=SPECK, noise=0):
    """Write a flat-register image with square dots planted at known places/sizes."""
    h, w = size[1], size[0]
    a = np.zeros((h, w, 3), dtype=np.uint8)
    a[:, :] = register
    if noise:
        rng = np.random.default_rng(7)
        a = np.clip(a.astype(int) + rng.integers(-noise, noise + 1, a.shape), 0, 255)
        a = a.astype(np.uint8)
    for (x, y, side) in dots:
        a[y:y + side, x:x + side] = speck
    Image.fromarray(a).save(path)
    return a


def _mask(path, size=(120, 160), inset=2):
    """A sub-frame figure mask. The inset is NOT cosmetic: a mask spanning the whole frame
    is exactly what the bbox ANDON refuses (E01's broken key reported a figure 751 px wide
    in a 752 px frame), so a fixture without it would be testing the guard, not the census.
    The full-frame case is built explicitly by the leg that asserts the guard fires."""
    w, h = size
    m = np.zeros((h, w), dtype=np.uint8)
    m[inset:h - inset, inset:w - inset] = 255
    Image.fromarray(m).save(path)
    return m


def _run(args):
    return subprocess.run([sys.executable, tool("twin_despeckle.py")] + args,
                          capture_output=True, text=True)


def _census(tmp_path, args):
    out = tmp_path / "c.json"
    r = _run(["--mode", "census", "--out-json", str(out)] + args)
    assert r.returncode == 0, "census failed:\n%s\n%s" % (r.stdout, r.stderr)
    return json.load(open(out))


# --- leg 1: exact censuses on planted fixtures ------------------------------------------

@pytest.mark.parametrize("dots,expect_n,expect_area", [
    ([(20, 30, 2), (60, 90, 3), (95, 20, 4)], 3, 4 + 9 + 16),
    ([(20, 30, 2)], 1, 4),
    ([], 0, 0),
])
def test_planted_census_is_exact(tmp_path, dots, expect_n, expect_area):
    img = tmp_path / "t.png"
    msk = tmp_path / "m.png"
    _plant(str(img), dots=dots)
    _mask(str(msk))
    rep = _census(tmp_path, ["--images", str(img), "--masks", str(msk)])
    row = rep["images"][0]
    assert row["count"] == expect_n, "planted %d dots, censused %d" % (expect_n, row["count"])
    assert row["total_area_px2"] == expect_area, \
        "planted %d px2, censused %d" % (expect_area, row["total_area_px2"])
    if dots:
        assert row["largest_px2"] == max(s * s for _, _, s in dots)


def test_planted_positions_are_recovered(tmp_path):
    """Not just the count - the blobs land where they were planted."""
    img, msk = tmp_path / "t.png", tmp_path / "m.png"
    _plant(str(img), dots=[(20, 30, 3), (70, 100, 3)])
    _mask(str(msk))
    rep = _census(tmp_path, ["--images", str(img), "--masks", str(msk)])
    got = sorted(tuple(b["bbox"][:2]) for b in rep["images"][0]["blobs"])
    assert got == [(20, 30), (70, 100)], got


# --- leg 2: the size threshold is an UPPER bound, and it discriminates -------------------

def test_a_region_is_rejected_and_the_speck_is_kept(tmp_path):
    """A 3x3 speck and a 20x20 region of the SAME colour. The speck is the class; the region
    is material, and a detector that counts it would flag a whole garment as speckle - the
    E07 failure in reverse.

    This leg caught the first implementation's real defect and is kept in the shape that
    caught it. Bounding the DEVIATION footprint let the region through: the local median is
    blind inside a structure wider than its window, so the 400 px2 block read as four 23 px2
    CORNERS, each under the threshold. The bound belongs on the colour structure. Both the
    exclusion count and the surviving blob's own structure area are asserted, so the region
    cannot pass by being invisible rather than by being rejected."""
    img, msk = tmp_path / "t.png", tmp_path / "m.png"
    _plant(str(img), dots=[(10, 10, 3), (60, 60, 20)])
    _mask(str(msk))
    rep = _census(tmp_path, ["--images", str(img), "--masks", str(msk)])
    row = rep["images"][0]
    assert row["count"] == 1, "expected only the 3x3 speck, got %d" % row["count"]
    assert row["total_area_px2"] == 9
    assert row["blobs"][0]["colour_structure_px2"] == 9, \
        "the surviving speck must be its own whole colour structure"
    assert row["diag"]["components_in_a_larger_colour_structure"] == 4, (
        "the region's four corner fragments must be counted as rejected, not silently "
        "absent: got %d" % row["diag"]["components_in_a_larger_colour_structure"])


def test_raising_blob_max_admits_the_region(tmp_path):
    """The companion: the same input under a threshold that spans it DOES admit it, so
    leg 2's exclusion is the threshold working rather than the region being invisible."""
    img, msk = tmp_path / "t.png", tmp_path / "m.png"
    _plant(str(img), dots=[(10, 10, 3), (60, 60, 20)])
    _mask(str(msk))
    rep = _census(tmp_path, ["--images", str(img), "--masks", str(msk),
                             "--blob-max-px2", "400", "--window", "41"])
    row = rep["images"][0]
    assert row["count"] == 2, row["count"]
    assert row["largest_px2"] == 400


# --- leg 3: can-fail. A clean register censuses ZERO ------------------------------------

def test_clean_register_censuses_zero(tmp_path):
    """If this ever returns non-zero on a flat register, every count above is noise."""
    img, msk = tmp_path / "t.png", tmp_path / "m.png"
    _plant(str(img), dots=[])
    _mask(str(msk))
    rep = _census(tmp_path, ["--images", str(img), "--masks", str(msk)])
    assert rep["images"][0]["count"] == 0
    assert rep["images"][0]["total_area_px2"] == 0


def test_noisy_but_speckless_register_censuses_zero(tmp_path):
    """+-6 of grain is not a speck. Discriminates against a detector keyed to any local
    minimum, which would return hundreds here."""
    img, msk = tmp_path / "t.png", tmp_path / "m.png"
    _plant(str(img), dots=[], noise=6)
    _mask(str(msk))
    rep = _census(tmp_path, ["--images", str(img), "--masks", str(msk)])
    assert rep["images"][0]["count"] == 0, \
        "grain read as %d specks" % rep["images"][0]["count"]


def test_a_brighter_blob_is_not_a_speck(tmp_path):
    """The class is DARK specks. A light blob of equal contrast must not count -
    discriminates against an unsigned |dE| detector."""
    img, msk = tmp_path / "t.png", tmp_path / "m.png"
    _plant(str(img), dots=[(30, 40, 3)], speck=(210, 170, 145))
    _mask(str(msk))
    rep = _census(tmp_path, ["--images", str(img), "--masks", str(msk)])
    assert rep["images"][0]["count"] == 0, "a LIGHT blob was censused as a dark speck"


# --- leg 4: the mask is honoured -------------------------------------------------------

def test_specks_outside_the_mask_are_not_censused(tmp_path):
    """A twin carries a painted backdrop. A dot there is not on the figure and must not
    enter a census whose denominator is the figure."""
    img = tmp_path / "t.png"
    msk = tmp_path / "m.png"
    _plant(str(img), dots=[(5, 5, 3), (60, 80, 3)])
    m = np.zeros((160, 120), dtype=np.uint8)
    m[40:140, 40:100] = 255            # excludes (5,5), includes (60,80)
    Image.fromarray(m).save(str(msk))
    rep = _census(tmp_path, ["--images", str(img), "--masks", str(msk)])
    row = rep["images"][0]
    assert row["count"] == 1, row["count"]
    assert row["blobs"][0]["bbox"][:2] == [60, 80]
    assert row["figure_px"] == int((m > 127).sum())


# --- leg 5: ANDONs FIRE on the wrong input ---------------------------------------------

def test_andon_mask_shape_mismatch_halts(tmp_path):
    img, msk = tmp_path / "t.png", tmp_path / "m.png"
    _plant(str(img))
    _mask(str(msk), size=(60, 60))
    r = _run(["--mode", "census", "--images", str(img), "--masks", str(msk)])
    assert r.returncode != 0
    assert "ANDON" in (r.stdout + r.stderr)


def test_andon_mask_count_mismatch_halts(tmp_path):
    a, b, msk = tmp_path / "a.png", tmp_path / "b.png", tmp_path / "m.png"
    _plant(str(a)); _plant(str(b)); _mask(str(msk))
    r = _run(["--mode", "census", "--images", str(a), str(b), "--masks", str(msk)])
    assert r.returncode != 0
    assert "parallel" in (r.stdout + r.stderr)


def test_andon_full_frame_mask_halts(tmp_path):
    """A figure cannot fill its frame. E01's bbox law, wired as a guard: the broken key
    it caught reported a figure 751 px wide in a 752 px frame."""
    img, msk = tmp_path / "t.png", tmp_path / "m.png"
    _plant(str(img))
    Image.fromarray(np.full((160, 120), 255, np.uint8)).save(str(msk))
    r = _run(["--mode", "census", "--images", str(img), "--masks", str(msk)])
    assert r.returncode != 0
    assert "spans the whole frame" in (r.stdout + r.stderr)


def test_andon_window_not_larger_than_blob_halts(tmp_path):
    """The median field must be robust to the specks it measures. A window at or below the
    largest kept blob's side would be estimated FROM the specks."""
    img, msk = tmp_path / "t.png", tmp_path / "m.png"
    _plant(str(img)); _mask(str(msk))
    r = _run(["--mode", "census", "--images", str(img), "--masks", str(msk),
              "--blob-max-px2", "400", "--window", "9"])
    assert r.returncode != 0
    assert "median field would be contaminated" in (r.stdout + r.stderr)


def test_the_same_call_succeeds_with_a_legal_window(tmp_path):
    """Companion to the four ANDON legs: the guarded path is reachable."""
    img, msk = tmp_path / "t.png", tmp_path / "m.png"
    _plant(str(img)); _mask(str(msk))
    r = _run(["--mode", "census", "--images", str(img), "--masks", str(msk),
              "--blob-max-px2", "400", "--window", "41"])
    assert r.returncode == 0, r.stderr


# --- leg 6: the report replays --------------------------------------------------------

def test_report_pins_every_parameter_and_input_hash(tmp_path):
    img, msk = tmp_path / "t.png", tmp_path / "m.png"
    _plant(str(img), dots=[(20, 30, 3)])
    _mask(str(msk))
    rep = _census(tmp_path, ["--images", str(img), "--masks", str(msk)])
    for k in ("blob_max_px2", "dark_dl", "de_min", "window", "log_sigmas"):
        assert k in rep["params"], k
    assert rep["tool_sha256"] and len(rep["tool_sha256"]) == 64
    assert rep["images"][0]["image_sha256"] and rep["images"][0]["mask_sha256"]
    assert rep["env"]["numpy"] and rep["env"]["scipy"]


def test_census_is_deterministic(tmp_path):
    img, msk = tmp_path / "t.png", tmp_path / "m.png"
    _plant(str(img), dots=[(20, 30, 3), (70, 100, 2)], noise=4)
    _mask(str(msk))
    a = _census(tmp_path, ["--images", str(img), "--masks", str(msk)])
    b = _census(tmp_path, ["--images", str(img), "--masks", str(msk)])
    assert a["images"][0]["blobs"] == b["images"][0]["blobs"]


# --- leg 7: the ANDONs survive -O and PYTHONOPTIMIZE ------------------------------------

@pytest.mark.parametrize("mode", ["-O", "env", "both"])
def test_andon_survives_optimize(tmp_path, mode):
    img, msk = tmp_path / "t.png", tmp_path / "m.png"
    _plant(str(img))
    Image.fromarray(np.full((160, 120), 255, np.uint8)).save(str(msk))
    cmd = [sys.executable]
    if mode in ("-O", "both"):
        cmd.append("-O")
    env = dict(os.environ)
    if mode in ("env", "both"):
        env["PYTHONOPTIMIZE"] = "1"
    r = subprocess.run(cmd + [tool("twin_despeckle.py"), "--mode", "census",
                              "--images", str(img), "--masks", str(msk)],
                       capture_output=True, text=True, env=env)
    assert r.returncode != 0, "the ANDON was DELETED under %s - it is not a gate" % mode
    assert "ANDON" in (r.stdout + r.stderr)


# --- leg 8: R-a. It FIRES on what the Director rejected, and is QUIET on the controls ----

REJECTED_TWINS = ["facet_E34\\twins\\twin_r3_v%d.png" % i for i in (1, 2, 3, 5, 6, 7)]
CLAY_CONTROLS = ["facet_E33\\turn_clay_300k\\armclay_%d.png" % i for i in (1, 2, 3)]


@pytest.mark.artifacts
def test_ra_fires_on_the_rejected_twins(assets, tmp_path):
    """R-a: the metric must separate what he rejected from what he did not. These are the
    twins carrying the class he ruled unacceptable at his zoom on 2026-08-14."""
    imgs, masks = [], []
    for rel in REJECTED_TWINS:
        v = rel.split("_v")[1].split(".")[0]
        imgs.append(str(need(assets, rel)))
        masks.append(str(need(assets, "facet_E34\\twin_control\\armclay_%s_mask.png" % v)))
    rep = _census(tmp_path, ["--images"] + imgs + ["--masks"] + masks)
    for row in rep["images"]:
        assert row["count"] > 0, \
            "the detector is BLIND on a rejected twin: %s" % row["image"]
    assert rep["totals"]["count"] > 0


@pytest.mark.artifacts
def test_ra_is_quiet_on_the_clay_controls(assets, tmp_path):
    """The other half, and the one that makes the first half mean something. The E34-seat
    attribution measured ZERO near-black px on the clay renders - the canny transmits no
    speck features, the generator invents them. A detector that also fires here is
    measuring the render, not the class."""
    imgs, masks = [], []
    for rel in CLAY_CONTROLS:
        v = rel.split("armclay_")[1].split(".")[0]
        imgs.append(str(need(assets, rel)))
        masks.append(str(need(assets, "facet_E34\\twin_control\\armclay_%s_mask.png" % v)))
    rep = _census(tmp_path, ["--images"] + imgs + ["--masks"] + masks)
    for row in rep["images"]:
        assert row["count"] == 0, (
            "the detector fired %d time(s) on a CLEAN clay control (%s) - it is not "
            "separating the class" % (row["count"], row["image"]))


@pytest.mark.artifacts
def test_ra_separation_is_not_an_artifact_of_the_mask(assets, tmp_path):
    """The twins and the clays are censused through the SAME masks, so a firing difference
    cannot be a difference in which pixels were looked at."""
    v = "1"
    m = str(need(assets, "facet_E34\\twin_control\\armclay_%s_mask.png" % v))
    twin = _census(tmp_path, ["--images", str(need(assets, "facet_E34\\twins\\twin_r3_v1.png")),
                              "--masks", m])
    clay = _census(tmp_path, ["--images", str(need(assets, "facet_E33\\turn_clay_300k\\armclay_1.png")),
                              "--masks", m])
    assert twin["images"][0]["figure_px"] == clay["images"][0]["figure_px"]
    assert twin["images"][0]["count"] > clay["images"][0]["count"]


@pytest.mark.artifacts
def test_recorded_trees_are_not_written(assets):
    """Census mode modifies no input. Cheap standing proof that this tool cannot move a
    recorded tree, since those trees have no revert."""
    p = need(assets, "facet_E34\\twins\\twin_r3_v1.png")
    before = (p.stat().st_size, p.stat().st_mtime_ns)
    m = need(assets, "facet_E34\\twin_control\\armclay_1_mask.png")
    r = _run(["--mode", "census", "--images", str(p), "--masks", str(m)])
    assert r.returncode == 0, r.stderr
    assert (p.stat().st_size, p.stat().st_mtime_ns) == before


def test_source_is_ascii():
    src = open(tool("twin_despeckle.py"), "rb").read()
    bad = [(i, b) for i, b in enumerate(src) if b > 127]
    assert not bad, "non-ASCII bytes at %s" % bad[:5]
